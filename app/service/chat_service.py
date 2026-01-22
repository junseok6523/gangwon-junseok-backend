# app/service/chat_service.py
import os
from langchain_upstage import ChatUpstage
from langchain_core.messages import HumanMessage, ToolMessage
from app.service.time_service import TimeService

class ChatService:
    def __init__(self, time_service: TimeService):
        # DI: 외부에서 TimeService를 주입받습니다.
        self.time_service = time_service
        # API 키가 환경변수에 없으면 에러가 날 수 있으니 확실히 로드
        self.llm = ChatUpstage(api_key=os.getenv("UPSTAGE_API_KEY"))

    def process_query(self, user_query: str) -> str:
        # 1. 도구(Tool) 정의
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_time",
                    "description": "특정 도시나 지역의 현재 시간을 조회합니다.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "시간을 알고 싶은 도시 이름 (예: 서울, 뉴욕, 런던)"
                            }
                        },
                        "required": ["location"]
                    }
                }
            }
        ]

        # 2. LLM에게 도구 바인딩 후 질문 던지기
        llm_with_tools = self.llm.bind_tools(tools)
        messages = [HumanMessage(content=user_query)]
        
        # 첫 번째 호출: AI가 도구를 쓸지 말지 결정
        response = llm_with_tools.invoke(messages)

        # 3. 도구 사용 요청이 있는지 확인 (Tool Calls)
        if hasattr(response, 'tool_calls') and response.tool_calls:
            # AI의 질문(도구 호출 요청)을 대화 내역에 반드시 추가해야 함!
            messages.append(response)
            
            # AI가 요청한 모든 도구 호출에 대해 루프를 돌며 응답 생성
            for tool_call in response.tool_calls:
                function_name = tool_call['name']
                arguments = tool_call['args']
                call_id = tool_call['id']  # 이 ID가 짝이 맞아야 에러가 안 남
                
                if function_name == "get_current_time":
                    location = arguments.get("location")
                    
                    # TimeService 호출 (결과 가져오기)
                    tool_result = self.time_service.get_current_time(location)
                    
                    # 결과 메시지 생성 (tool_call_id를 꼭 넣어줘야 함)
                    tool_msg = ToolMessage(content=str(tool_result), tool_call_id=call_id)
                    messages.append(tool_msg)
            
            # 4. 도구 결과를 포함한 대화 내역으로 다시 LLM 호출 (최종 답변)
            final_response = self.llm.invoke(messages)
            return final_response.content
        
        # 도구를 안 썼다면 그냥 답변 반환
        return response.content