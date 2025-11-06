from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence,RunnableParallel

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    task="text-generation",

)

model1 = ChatHuggingFace(llm=llm)

model2 = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

parser = StrOutputParser()

parser = StrOutputParser()
prompt1 = PromptTemplate(
    template='Generate a tweet on  {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template="Generate a linkdin short post on {topic}",
    input_variables=['topic']
)

chain = RunnableParallel(
    chain1 = prompt1 | model1 | parser,
    chain2 = prompt2 | model2 | parser
)

result = chain.invoke({'topic':'AI'})
print(f'Tweet : {result['chain1']}')
print(f'Linkdin Post : {result['chain2']}')
