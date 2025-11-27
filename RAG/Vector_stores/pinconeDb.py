# -----------------------------------------------------------
# 1. IMPORTS
# -----------------------------------------------------------
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEndpointEmbeddings
import os
from langchain_core.prompts import PromptTemplate

from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from pinecone import Pinecone ,ServerlessSpec
from dotenv import load_dotenv

load_dotenv()


# -----------------------------------------------------------
# 2. EMBEDDING MODEL (dimension depends on model)
# -----------------------------------------------------------
embeddings = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)


# ensure key present
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
if not PINECONE_API_KEY:
    raise SystemExit("Missing PINECONE_API_KEY in environment. Set it in .env or export PINECONE_API_KEY.")

# -----------------------------------------------------------
# 3. CREATE PINECONE INDEX (only once)
# -----------------------------------------------------------
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "genai"

# Create index only if not exist
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )


# Connect to created index
index = pc.Index(index_name)

# -----------------------------------------------------------
# 4. SAMPLE RAW DOCUMENTS
# -----------------------------------------------------------
raw_docs = [
    "Pinecone is a vector database used for similarity search.",
    "LangChain is a framework for building LLM applications.",
    "Namespaces in Pinecone separate different datasets logically.",
]

# Convert to Document objects (LangChain standard)
docs = [Document(page_content=d) for d in raw_docs]

# -----------------------------------------------------------
# 5. SPLIT DOCUMENTS INTO CHUNKS (recommended)
# -----------------------------------------------------------
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
chunked_docs = splitter.split_documents(docs)

# -----------------------------------------------------------
# 6. ADD DOCUMENTS TO PINECONE (METHOD 1: from_documents)
# -----------------------------------------------------------
vectorstore = PineconeVectorStore.from_documents(
    documents=chunked_docs,
    embedding=embeddings,
    index_name=index_name,  
    namespace="main_data"     # namespace 1
)


#  add.document is also used to add document in existing index
# vectorstore.add_documents(documents=chunked_docs) 

# -----------------------------------------------------------
# 7. ADD MORE DOCUMENTS (METHOD 2: from_existing_documents)
#    Useful when the index already exists
# -----------------------------------------------------------
extra_docs = [
    Document(page_content="Retrieval Augmented Generation improves accuracy."),
    Document(page_content="Pinecone works with any embedding model.")
]

vectorstore2 = PineconeVectorStore.from_existing_index(
    embedding=embeddings,
    index_name=index_name,
    namespace="extra_data"    # DIFFERENT namespace
)

# -----------------------------------------------------------
# 8. BASIC RETRIEVER (namespace = main_data)
# -----------------------------------------------------------
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3, "namespace": "main_data"}
)


# -----------------------------------------------------------
# 9. LANGCHAIN RETRIEVAL-QA CHAIN (The LLM Connection) 🧠
# -----------------------------------------------------------
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# 9.1 Define the Prompt Template

template = PromptTemplate(
    input_variables=["context , question"],
    template=""""
    You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved to answer the question. "
    "If you don't know the answer, just say that you don't know."
      
        [Transcript Context]
        {context}

        [User Question]
        {question}
        """

)

parallel_chain = RunnableParallel({
 "context":retriever,
 "question":RunnablePassthrough()
})


parser = StrOutputParser()

query = parallel_chain | template | llm | parser

result = query.invoke("what is pinecone")

print(result)

# -----------------------------------------------------------
# 10. METADATA FILTERING (ADVANCED)
# -----------------------------------------------------------

# Add documents with metadata
# meta_docs = [
#     Document(page_content="Pinecone uses cosine similarity.", metadata={"topic": "pinecone"}),
#     Document(page_content="LangChain creates LLM pipelines.", metadata={"topic": "langchain"}),
# ]

# vectorstore3 = PineconeVectorStore.from_documents(
#     documents=meta_docs,
#     embedding=embeddings,
#     index_name=index_name,
#     namespace="meta_data"
# )

# # Retriever with metadata filter
# meta_retriever = vectorstore3.as_retriever(
#     search_type="similarity",
#     search_kwargs={
#         "k": 5,
#         "namespace": "meta_data",
#         "filter": {"topic": "pinecone"}   # ONLY retrieve Pinecone docs
#     }
# )

# response2 = meta_retriever.invoke("Explain Pinecone")
# print("\n🔵 Metadata Filter Output:", response2)

# # -----------------------------------------------------------
# # 11. DELETE VECTORS FROM A NAMESPACE
# # -----------------------------------------------------------main_data
# # delete_all=True clears entire namespace
# # pc.Index(index_name).delete(
# #     delete_all=True,
# #     namespace="extra_data"
# # )

# print("\n⚠️ 'extra_data' namespace deleted")

# # -----------------------------------------------------------
# # 12. END-TO-END RAG PIPELINE (FINAL)
# # -----------------------------------------------------------
# query = "Explain RAG in simple language."

# final_answer = qa_chain.invoke({"query": query})
# print("\n🟢 FINAL RAG ANSWER:", final_answer["result"])