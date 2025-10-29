from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
template = PromptTemplate(
    input_variables=["topic"],
    template="Explain {topic} in simple words."
)

# Combine both directly
chain = template | model

result = chain.invoke({"topic": "quantum computing"})
print(result.content)
