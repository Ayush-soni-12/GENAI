from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableBranch ,RunnableLambda
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

# --- Models ---
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    task="text-generation",
)

model1 = ChatGoogleGenerativeAI(model="gemini-2.5-flash")  # for classification
model2 = ChatHuggingFace(llm=llm)  # for response generation

# --- Schema for structured output ---
class Feedback(BaseModel):
    sentiments: Literal["positive", "negative"] = Field(
        description="Give the sentiment of the feedback"
    )

# --- Prompt for classification ---
prompt = PromptTemplate(
    template="Classify the feedback as positive or negative only:\n{feedback}",
    input_variables=["feedback"],
)

# --- Chain for sentiment classification ---
structured_classifier = model1.with_structured_output(Feedback)
classifier_chain = prompt | structured_classifier

# --- Prompts for generating responses ---
prompt_positive = PromptTemplate(
    template="Write an appropriate and friendly response to this positive feedback:\n{feedback}",
    input_variables=["feedback"],
)

prompt_negative = PromptTemplate(
    template="Write an appropriate and polite response to this negative feedback:\n{feedback}",
    input_variables=["feedback"],
)

# --- Branching logic ---
branch_chain = RunnableBranch(
    (
        lambda x: x.sentiments == "positive",
        prompt_positive | model2,
    ),
    (
        lambda x: x.sentiments == "negative",
        prompt_negative | model2,
    ),
    RunnableLambda(lambda x: "could not find sentiment")
)

# --- Final chain combining everything ---
final_chain = classifier_chain | branch_chain

# --- Run the full chain ---
feedback_text = "this is a good phone"

result = final_chain.invoke({"feedback": feedback_text})
print("Feedback:", feedback_text)
print("Model Response:\n", result.content)
