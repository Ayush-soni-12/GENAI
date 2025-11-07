from langchain_community.document_loaders import TextLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()


loader = TextLoader('documents/plain_text.txt',encoding='utf-8')

docs = loader.load()


model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

prompt = PromptTemplate(
    template = 'generate a  short summary  on this  paragraph  {text}',
    input_variables= ['text']
)

parser = StrOutputParser()

chain = prompt | model | parser

text = docs[0].page_content

result =  chain.invoke({'text':text})

print(result)



