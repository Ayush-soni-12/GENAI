import os
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Set a User-Agent so your request isn’t blocked
os.environ["USER_AGENT"] = "MyLangChainApp/1.0"

url = 'https://www.life.com/arts-entertainment/harry-potter-the-story-that-changed-the-world/'

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

loader = WebBaseLoader(url)
docs = loader.load()

parser = StrOutputParser()

Prompt = PromptTemplate(
    template='Answer the following question {question} on this text {text}',
    input_variables=['question','text']
)

chain = Prompt |model | parser

result = chain.invoke({'question':'total gross value of this film','text':docs[0].page_content})

print(result)