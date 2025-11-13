from youtube_transcript_api import YouTubeTranscriptApi,TranscriptsDisabled
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_classic.prompts import PromptTemplate
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()


app = FastAPI()


# Allow extension access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for local dev; later restrict to chrome-extension://id
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str
    videoId: str

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

@app.post("/ask")
async def ask_ai(req: AskRequest):
    """Handle AI question from Chrome extension"""
    user_input = f"Video ID: {req.videoId}\nUser question: {req.question}"
    
    try:
        response = model.invoke(user_input)
        answer = response.content
        # print(f"Answer : ",answer)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}