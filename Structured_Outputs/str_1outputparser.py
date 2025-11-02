from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


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

parser = StrOutputParser()

chain = template1 | model | parser | template2 | model | parser

result = chain.invoke({"topic":"black hole"})

print(result)