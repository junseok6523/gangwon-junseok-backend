# app/routers/chat.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.service.chat_service import ChatService
from app.service.time_service import TimeService

router = APIRouter()

# 요청/응답 스키마 정의
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# 의존성 주입 (Dependency Injection) 설정
# Router -> ChatService -> TimeService 순서로 조립됩니다.
def get_chat_service():
    time_service = TimeService()
    return ChatService(time_service)

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, service: ChatService = Depends(get_chat_service)):
    answer = service.process_query(request.message)
    return ChatResponse(response=answer)