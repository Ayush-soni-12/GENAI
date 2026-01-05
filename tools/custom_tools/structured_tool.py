from langchain_community.tools import StructuredTool
from pydantic import BaseModel , Field


class MultiplyInput(BaseModel):
    a:int = Field(required=True,description="The first number to add"),
    b:int = Field(required=True,description="The second number to add")

def Multiply_func(a:int,b:int) -> int:
    return a*b


multiply_tool = StructuredTool.from_function(
    func=Multiply_func,
    name="multiply",
    description="Multiply two numbers",
    args_schema=MultiplyInput
)


result = multiply_tool.invoke({'a':3, 'b':3})

print(f"Results : ",result)
print(multiply_tool.name)
print(multiply_tool.description)
print(multiply_tool.args)