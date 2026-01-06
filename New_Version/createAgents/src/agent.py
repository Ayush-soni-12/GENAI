from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
import requests
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import HumanMessage,ToolMessage
from dotenv import load_dotenv

load_dotenv()


@wrap_tool_call
def handle_tool_errors(request, handler):
    """Handle tool execution errors with custom messages."""
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({str(e)})",
            tool_call_id=request.tool_call["id"]
        )




@tool('get_current_weather' ,description="Get the current weather in a given location",return_direct=False)
def get_current_weather(city:str)->str:
    response = requests.get(f"https://wttr.in/{city}?format=j1", timeout=10)
    response.raise_for_status()
    return response.json()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.1,
    max_output_tokens=1024,
)


# llm = HuggingFaceEndpoint(
#     repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
#     task="chat-completion",
#     temperature=0.1,
#     max_new_tokens=512,
# )

# model = ChatHuggingFace(llm=llm)


agent = create_agent(
    model=model,
    tools=[get_current_weather],
    system_prompt="you are a helpful assistant that can provide the weather of any city",
    middleware=[handle_tool_errors]
)

response = agent.invoke({'messages':[HumanMessage(content="weather in New York City")]})
answer = response['messages'][-1].content
print('AI RESPONSE:',answer)