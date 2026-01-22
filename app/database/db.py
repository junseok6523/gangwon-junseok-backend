import os
import chromadb

# Docker 환경에서는 'chroma-server'라는 컨테이너 이름으로 접속합니다.
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", 8000))

def get_chroma_client():
    # HttpClient를 사용해야 별도로 뜬 DB 컨테이너와 통신할 수 있습니다.
    return chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)