If LLM supports the structured output - Then we can use the with_Structured_output function. But some LLM’s does not support it - For this case, we have to use the output parser



Output Parsers in LangChain help convert raw LLM responses into structured formats like JSON, CSV, Pydantic models and more. They ensure consistency, validation and ease of use in applications.



There are many parsers in the Langchain.



*Here we are discussing:*



1. StrOutputParser - For string output

2. JSONOutputParser - Json output - But not structured

3. StructuredOutputParser - Structured Json - But No validation

4. PydanticOutputParser - Structured Json and Validated



### StrOutputParser



This is the simplest output parser. it is used to parse the output of the LLM and return it as a plain string.



- It is useful, If we want to create the chains



### JSONOutputParser



Outputs the json format



- But drawback is we cannot enforce the specific schema output we want.

- Json format is decided my the LLM only



### StructuredOutputParser



It helps extract structured JSON data from LLM responses based on the predefined field schemas.



It returns in the required format, But it doesn’t validate.



Example: We want age as int (7). But this parser will accept even if age is str (7 years)



### PydanticOutputParser



StructuredOutputParser that uses Pydantic models to enforce schema validation when processing LLM responses.



*Why Use this?*



- Strict schema enforcement

- Type safety

- Easy validation

- Seamless integration