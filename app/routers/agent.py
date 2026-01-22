from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.service.agent_service import AgentService
from app.dependencies import get_agent_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat_endpoint(req: ChatRequest, service: AgentService = Depends(get_agent_service)):
    return {"response": service.process_query(req.message)}

@router.post("/knowledge")
def load_knowledge_endpoint(service: AgentService = Depends(get_agent_service)):
    return {"status": service.load_rules_to_db()}