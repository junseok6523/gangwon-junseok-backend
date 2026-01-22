from app.repository.client.upstage_client import UpstageClient
from app.service.chat_service import ChatService
from fastapi import Depends

upstage_client = UpstageClient()


def get_upstage_client() -> UpstageClient:
    return upstage_client


def get_chat_service(upstage_client: UpstageClient = Depends(get_upstage_client)) -> ChatService:
    return ChatService(upstage_client)
