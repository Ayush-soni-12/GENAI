from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
import requests
from langchain.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()


@tool('get_current_weather' ,description="Get the current weather in a given location",return_direct=False)
def get_current_weather(city:str)->str:
   response =  requests.get(f"https://wttr.in/{city}?format=3")
   return response.text

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.1,
    max_output_tokens=1024,
)

agent = create_agent(model=model,tools=[get_current_weather])

response = agent.invoke({'messages':[HumanMessage(content="Hello")]})
answer = response['messages'][-1].content
print('AI RESPONSE:',answer)