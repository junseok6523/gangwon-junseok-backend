import uuid
from langchain_chroma import Chroma
from app.database.db import get_chroma_client
from app.service.embedding_service import EmbeddingService

class VectorRepository:
    def __init__(self, embedding_service: EmbeddingService):
        self.client = get_chroma_client()
        self.embedding_function = embedding_service.get_embedding_function()
        
        # 'rules_collection'이라는 이름으로 저장소 공간 확보
        self.vector_store = Chroma(
            client=self.client,
            collection_name="rules_collection",
            embedding_function=self.embedding_function
        )

    def add_documents(self, texts: list[str], metadatas: list[dict]):
        # 문서마다 고유 ID를 부여해서 저장
        ids = [str(uuid.uuid4()) for _ in range(len(texts))]
        self.vector_store.add_texts(texts=texts, metadatas=metadatas, ids=ids)

    def search_similar(self, query: str, k: int = 1):
        # 질문과 가장 유사한 내용 검색
        return self.vector_store.similarity_search(query, k=k)