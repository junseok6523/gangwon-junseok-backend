from app.service.time_service import TimeService
from app.service.embedding_service import EmbeddingService
from app.repository.vector_repo import VectorRepository
from app.service.agent_service import AgentService

def get_agent_service():
    time_svc = TimeService()
    embed_svc = EmbeddingService()
    repo = VectorRepository(embed_svc)
    return AgentService(time_svc, repo)