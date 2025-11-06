from unittest import result
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence,RunnableParallel,RunnablePassthrough

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    task="text-generation",

)

model1 = ChatHuggingFace(llm=llm)

model2 = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

parser = StrOutputParser()

prompt1 = PromptTemplate(
    template='Generate a joke on  {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template= 'write a short explaination on text {text}',
    input_variables=['text']
)

joke_chain = RunnableSequence(prompt1,model1,parser)

parallel_chain = RunnableParallel(
    chain1 = RunnablePassthrough(),
    chain2 = RunnableSequence(prompt2,model2,parser)

)

chain = joke_chain | parallel_chain
result = chain.invoke({'topic':'AI'})

print("JOKE : ",result['chain1'])
print("EXPLAINATION : " , result['chain2'])