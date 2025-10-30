from typing import TypedDict

class Person(TypedDict):
    name:str
    age:int

newPerson:Person = {
    'name' : "Ayush",
    'age' : 32
}

print(newPerson)

# typeDic is a way to create  dictiinory in python
# . This brings type-hinting capabilities to dictionaries, allowing static type checkers like MyPy to verify the structure and types of dictionary data at development time.