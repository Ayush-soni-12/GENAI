from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    task="text-generation",

)

model = ChatHuggingFace(llm=llm)


template1 = PromptTemplate(
    template = "Write a summary on {topic}",
    input_variables=["topic"]
)

template2 = PromptTemplate(
    template = "write a 5 line summary on text {text}",
    input_variables=["text"]
)

 
chain1 = template1 | model
result1 = chain1.invoke({"topic":"black hole"})

chain2 = template2 | model
result2 = chain2.invoke({'text':result1.content})

print(result2.content)

