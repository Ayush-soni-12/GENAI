from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt = PromptTemplate(
    template='Generate 5 interesting fact about {topic}',
    input_variables=['topic']
)

parser = StrOutputParser()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

chain = prompt | model | parser

result = chain.invoke({"topic":"cricket"})

print(result)