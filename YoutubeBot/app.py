from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_community.document_loaders import YoutubeLoader
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI , GoogleGenerativeAIEmbeddings
from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor
from langchain_chroma import Chroma
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    question: str
    videoId: str


embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

@app.post("/ask")
async def ask_ai(req: AskRequest):
    try:
        # ✅ Ask youtube_transcript_api to translate directly
        loader = YoutubeLoader.from_youtube_url(
            f"https://www.youtube.com/watch?v={req.videoId}",
             language=["en", "id","hi"],

        )

        docs = loader.load()

        if not docs:
            raise Exception("No transcript found or translation not available for this video.")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200
        )
        chunks = splitter.split_documents(docs)

        # print("Chunks : ",chunks)

        transcript_text = " ".join([chunk.page_content for chunk in chunks])
        print("✅ Final Transcript (Auto-Translated to English):\n")
        # print(transcript_text[:1000], "...")

        # 4. Create (or load) a Chroma vector store
        vector_store = Chroma( 
            collection_name="Chroma_collection",
            embedding_function=embeddings,
        )

        vector_store.add_documents(chunks)

        multiquery_retriever = MultiQueryRetriever.from_llm(
        retriever=vector_store.as_retriever(search_type="similarity",search_kwargs={"k": 5}),
        llm= ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        )

        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        compressor = LLMChainExtractor.from_llm(llm)

        compression_retriever = ContextualCompressionRetriever(
            base_retriever=multiquery_retriever,
            base_compressor=compressor
        )  

        prompt = PromptTemplate(
            template="""
        You are an intelligent and insightful AI assistant specialized in analyzing YouTube videos.

        Your task:
        - Use only the transcript context provided below.
        - Understand the tone, meaning, and intent behind the video content.
        - If the answer can be inferred, explain it clearly and naturally.
        - If the context is not enough, say: "The transcript doesn’t include enough details to answer this."

        Guidelines:
        - Think step-by-step before answering.
        - Combine related information from different parts of the transcript if helpful.
        - Never invent facts or assume things not in the transcript.
        - If the user asks for opinions, summaries, key points, or explanations — provide them clearly and concisely.
        - If the question is general but relevant to the video’s topic, relate your answer to the video content intelligently.

        ----------------------------
        [Transcript Context]
        {context}

        [User Question]
        {question}

        Now give a clear, well-structured answer:
        """,
            input_variables=["context", "question"]
        )

        parallel_chain = RunnableParallel({
            "context":compression_retriever,
            "question":RunnablePassthrough()
        })

        parser = StrOutputParser()

        main_chain  = parallel_chain | prompt | llm | parser

        result = main_chain.invoke(req.question)

        return {"answer": result}
    except Exception as e:
        return {"error :",e}
