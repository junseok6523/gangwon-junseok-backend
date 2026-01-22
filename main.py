from fastapi import FastAPI
from dotenv import load_dotenv
from app.routers import agent

load_dotenv()
app = FastAPI()

app.include_router(agent.router, prefix="/api/v1", tags=["agent"])

@app.get("/")
def root():
    return {"message": "AI Agent Service with Docker & RAG is Running!"}