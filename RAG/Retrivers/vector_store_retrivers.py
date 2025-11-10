from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_classic.schema import Document
from dotenv import load_dotenv

# 1. Load environment variables (for Google API key)
load_dotenv()

# 2. Initialize embedding model
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# 3. Create documents
doc1 = Document(
    page_content="Artificial Intelligence (AI) is a branch of computer science focused on building machines that can perform tasks requiring human intelligence.",
    metadata={"topic": "AI", "source": "Wikipedia", "length": "short", "category": "technology"}
)
doc2 = Document(
    page_content="Machine learning enables systems to learn and improve from experience without being explicitly programmed.",
    metadata={"topic": "Machine Learning", "source": "Blog Article", "length": "medium", "category": "education"}
)
doc3 = Document(
    page_content="Deep learning is a subset of machine learning that uses neural networks with many layers to analyze various levels of data abstraction.",
    metadata={"topic": "Deep Learning", "source": "Research Paper", "length": "long", "category": "AI"}
)
doc4 = Document(
    page_content="Natural Language Processing (NLP) allows computers to understand, interpret, and respond to human language.",
    metadata={"topic": "NLP", "source": "Online Course", "length": "medium", "category": "AI Applications"}
)
doc5 = Document(
    page_content="Computer vision enables computers to extract meaningful information from images, videos, and other visual inputs.",
    metadata={"topic": "Computer Vision", "source": "Tech Journal", "length": "short", "category": "AI Applications"}
)

docs = [doc1, doc2, doc3, doc4, doc5]

# 4. Create (or load) a Chroma vector store
vector_store = Chroma( 
    collection_name="Chroma_collection",
    embedding_function=embeddings,
)



# 5. Add documents into Chroma


vector_store.add_documents(docs)

#  this thing also work if we use similarity_search function in vector store but the benefit of using retrivers are multiples
# 1 retrivers are runnable so we connect them easily with other components and make chains
# 2 with the help of retrivers we use many algorithm to search the relevant query but in similarity_search only one algo follow it match all vector 


# retrivers = vector_store.as_retriever(search_kwargs={"k":2})

retrivers = vector_store.as_retriever(
    search_type="mmr", # this enable mmr it is a technique to get relvant document it first pick the most releavent document then it again pick the relevent document but it is less similar to first document through this way same meaning of document avoid
    search_kwargs={"k":2,"lambda_mult":0.5}

    
)



query = "What is AI"

results = retrivers.invoke(query)

for i ,result in enumerate(results):
    print(f"Result {i+1 } : ", result.page_content)

