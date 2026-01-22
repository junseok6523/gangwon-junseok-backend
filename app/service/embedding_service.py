import os
from langchain_upstage import UpstageEmbeddings

class EmbeddingService:
    def __init__(self):
        # 텍스트를 숫자로 바꿔주는 모델 (Solar Embedding)
        self.embeddings = UpstageEmbeddings(
            api_key=os.getenv("UPSTAGE_API_KEY"),
            model="solar-embedding-1-large"
        )

    def get_embedding_function(self):
        return self.embeddings