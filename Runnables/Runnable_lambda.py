
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence,RunnableLambda , RunnablePassthrough , RunnableParallel



load_dotenv()

prompt = PromptTemplate(
    template='write  a joke on {topic}',
    input_variables=['topic']
)

parser = StrOutputParser()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

Joke_chain = RunnableSequence(prompt,model,parser)

parallel_chain  = RunnableParallel(
    chain1 = RunnablePassthrough(),
    chain2 = RunnableLambda(lambda x : len(x.split()))

)

chain = Joke_chain |  parallel_chain
result = chain.invoke({'topic':'AI'})

print(f'JOKE : {result['chain1']}')
print(f'COUNT : {result['chain2']}')
