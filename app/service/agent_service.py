import json
from langchain_upstage import ChatUpstage
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from app.service.time_service import TimeService
from app.repository.vector_repo import VectorRepository

class AgentService:
    def __init__(self, time_service: TimeService, vector_repo: VectorRepository):
        self.time_service = time_service
        self.vector_repo = vector_repo
        self.llm = ChatUpstage()

    def load_rules_to_db(self):
        """rules.json을 읽어서 DB에 적재"""
        try:
            with open("rules.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            
            texts = [item["description"] for item in data]
            metadatas = [{"office": item["office"]} for item in data]
            
            self.vector_repo.add_documents(texts, metadatas)
            return "규정 데이터 로드 완료!"
        except Exception as e:
            return f"데이터 로드 실패: {str(e)}"

    def process_query(self, user_query: str) -> str:
        # 1. RAG: 질문과 관련된 규정 검색
        docs = self.vector_repo.search_similar(user_query)
        rule_context = docs[0].page_content if docs else "관련 규정 없음"

        # 2. 시스템 프롬프트 구성 (지식 주입)
        system_prompt = f"""
        당신은 회사 근무 규정 안내 봇입니다. 
        [검색된 규정]을 기반으로 답변하되, 시간이 필요한 질문이면 도구를 사용해 확인하세요.

        [검색된 규정]
        {rule_context}
        """

        # 3. 도구(Tool) 정의
        tools = [{
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "도시의 현재 시간을 조회합니다.",
                "parameters": {
                    "type": "object",
                    "properties": {"location": {"type": "string"}},
                    "required": ["location"]
                }
            }
        }]

        # 4. LLM 호출
        llm_with_tools = self.llm.bind_tools(tools)
        messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_query)]
        response = llm_with_tools.invoke(messages)

        # 5. Tool Call 처리
        if hasattr(response, 'tool_calls') and response.tool_calls:
            messages.append(response)
            for tool in response.tool_calls:
                if tool['name'] == "get_current_time":
                    loc = tool['args'].get('location')
                    result = self.time_service.get_current_time(loc)
                    messages.append(ToolMessage(content=result, tool_call_id=tool['id']))
            
            # 도구 결과 포함하여 최종 답변
            final = self.llm.invoke(messages)
            return final.content
            
        return response.content