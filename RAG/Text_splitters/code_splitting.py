from langchain_text_splitters import RecursiveCharacterTextSplitter , Language 

text = """
class Dog:
    # Class attribute (shared by all instances of Dog)
    species = "Canine"

    # Constructor method to initialize instance attributes
    def __init__(self, name, age):
        self.name = name  # Instance attribute
        self.age = age    # Instance attribute

    # Instance method to define behavior
    def bark(self):
        print(f"{self.name} says Woof!")

    def describe(self):
        print(f"{self.name} is a {self.species} and is {self.age} years old.")

# Creating instances (objects) of the Dog class
my_dog = Dog("Buddy", 3)
another_dog = Dog("Lucy", 5)

# Accessing attributes and calling methods
print(f"My dog's name is {my_dog.name}.")
my_dog.bark()
my_dog.describe()

print(f"Another dog's name is {another_dog.name}.")
another_dog.bark()
another_dog.describe()

print(f"All dogs are {Dog.species}.")
"""

splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size = 500,
    chunk_overlap = 0,
)

results = splitter.split_text(text)

for  index , result in enumerate(results):
    print(f"line {index} : {result}")   