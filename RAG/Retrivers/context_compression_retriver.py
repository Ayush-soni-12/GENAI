from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_classic.schema import Document
from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor
from dotenv import load_dotenv 

# 1. Load environment variables (for Google API key)
load_dotenv()

# 2. Initialize embedding model
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

docs = [
    Document(page_content=(
        """The Grand Canyon is one of the most visited natural wonders in the world.
        Photosynthesis is the process by which green plants convert sunlight into energy.
        Millions of tourists travel to see it every year. The rocks date back millions of years."""
    ), metadata={"source": "Doc1"}),

    Document(page_content=(
        """In medieval Europe, castles were built primarily for defense.
        The chlorophyll in plant cells captures sunlight during photosynthesis.
        Knights wore armor made of metal. Siege weapons were often used to breach castle walls."""
    ), metadata={"source": "Doc2"}),

    Document(page_content=(
        """Basketball was invented by Dr. James Naismith in the late 19th century.
        It was originally played with a soccer ball and peach baskets. NBA is now a global league."""
    ), metadata={"source": "Doc3"}),

    Document(page_content=(
        """The history of cinema began in the late 1800s. Silent films were the earliest form.
        Thomas Edison was among the pioneers. Photosynthesis does not occur in animal cells.
        Modern filmmaking involves complex CGI and sound design."""
    ), metadata={"source": "Doc4"})
]


# 4. Create (or load) a Chroma vector store
vector_store = Chroma( 
    collection_name="Chroma_collection",
    embedding_function=embeddings,
)



# 5. Add documents into Chroma


vector_store.add_documents(docs)

# some time when user ask query it meaning does not exact clear there are many meaning of that query so sometime model got confused for solve this problem we use multi query retriver
#  this retriver generate a more query based on user query and after that relevant document find for that query which it generate


similarity_retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
compressor = LLMChainExtractor.from_llm(llm)

compression_retriever = ContextualCompressionRetriever(
    base_retriever=similarity_retriever,
    base_compressor=compressor
)

# Query the retriever
query = "What is photosynthesis?"
compressed_results = compression_retriever.invoke(query)

for i, doc in enumerate(compressed_results):
    print(f"\n--- Result {i+1} ---")
    print(doc.page_content)