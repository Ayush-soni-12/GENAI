# from langchain_huggingface import HuggingFaceEmbeddings


# embedding = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2')
# text = "Delhi is the captial of India"

# vector = embedding.embed_query(text)

# print(str(vector))

from langchain_huggingface import HuggingFaceEndpointEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

embeddings = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

vector = embeddings.embed_documents(["Delhi is the capital of India","hello"])
print(str(vector))  # print first 10 values

