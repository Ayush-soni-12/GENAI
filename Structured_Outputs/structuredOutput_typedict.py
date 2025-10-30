from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from typing import TypedDict

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    task="text-generation",
)



model = ChatHuggingFace(llm=llm)

# Schema 

class Review(TypedDict):
    summary:str
    sentiment:str

structured_model = model.with_structured_output(Review)


input_text = (
    "\"I bought this product last month and it works exactly as advertised. "
    "The battery life is great and the build quality feels premium. Highly recommended!\""
)
result = structured_model.invoke(input_text)
print(result)