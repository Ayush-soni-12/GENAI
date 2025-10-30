from pydantic import BaseModel
from typing import Optional

class Student(BaseModel):
    name:str="Aman"
    age: Optional[int] = None




student = Student(name="Ayush")
print(student)