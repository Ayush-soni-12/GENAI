from json import load
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv


load_dotenv()


@tool
def multiply(a:int,b:int)->int:
    """Multiply the number a and b """
    return a*b


llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

llm_with_tools = llm.bind_tools([multiply])

query = HumanMessage('multiply 7 with 8')

message = [query]

result = llm_with_tools.invoke(message)

message.append(result)

tool_result = multiply.invoke(result.tool_calls[0])

message.append(tool_result)

final_result = llm_with_tools.invoke(message)

print(final_result.content)