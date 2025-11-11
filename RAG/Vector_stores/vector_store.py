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
    persist_directory="./chroma_langchain_db",  # directory where data is saved
)

# 5. Add documents into Chroma


# vector_store.add_documents(docs)


print("✅ Documents successfully embedded and saved to ./chroma_langchain_db")

# 7. Test a query
query = "What is machine learning?"


#  for view the documents we also see embeddings and metadatas

# view_db = vector_store.get(include=['documents'])

# print(view_db)

#  we also update the documents

updated_doc1 = Document(
    page_content="I am Ayush soni i am genius",
    metadata={'Founder':'AI'}
)

Document_update = vector_store.update_document(document_id='3b29b2e5-d6c6-400a-b47d-f5c30bfa2d7f',document=updated_doc1)

print('Update :',Document_update )

view_db = vector_store.get(include=['documents'])

print(view_db)

#  we also delete the data 

Delete_document = vector_store.delete(ids=['3b29b2e5-d6c6-400a-b47d-f5c30bfa2d7f'])

view_db = vector_store.get(include=['documents'])

print(view_db)

#  based on query

# results = vector_store.similarity_search(query, k=2) #it is query based

# print("\n🔍 Query Results:")
# for i, res in enumerate(results):
#     print(f"\nResult {i+1}:")
#     print("Content:", res.page_content)
#     print("Metadata:", res.metadata)



# # based on filter 

# results = vector_store.similarity_search_with_score(
#     query='Explain AI concepts',
#     filter={'topic': 'AI'}
# )

# print("\n🔍 Query Results:")
# for i, (doc, score) in enumerate(results, 1):
#     print(f"Result {i}:")
#     print("Content:", doc.page_content)
#     print("Metadata:", doc.metadata)
#     print("Score:", score)