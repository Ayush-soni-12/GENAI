from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a grammar corrector."),
    ("user", "Fix grammar: {text}")
])

chain = prompt | model

result = chain.invoke({"text": "He go to school everyday"})
print(result.content)
