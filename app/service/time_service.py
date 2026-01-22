# app/service/time_service.py
import requests
from datetime import datetime
import pytz # 시스템 설정 무시하고 자체 DB 사용

class TimeService:
    def __init__(self):
        # 한글, 영어 대소문자 모두 커버하는 방탄 매핑
        self.timezone_map = {
            "서울": "Asia/Seoul", "seoul": "Asia/Seoul", "korea": "Asia/Seoul",
            "런던": "Europe/London", "london": "Europe/London", "uk": "Europe/London",
            "뉴욕": "America/New_York", "new york": "America/New_York", "ny": "America/New_York",
            "파리": "Europe/Paris", "paris": "Europe/Paris",
            "도쿄": "Asia/Tokyo", "tokyo": "Asia/Tokyo",
            "베이징": "Asia/Shanghai", "beijing": "Asia/Shanghai"
        }

    def get_current_time(self, location: str) -> str:
        # 1. 도시명 표준화
        clean_loc = location.strip().lower()
        timezone = self.timezone_map.get(clean_loc)
        
        # 매핑에 없으면 원본 그대로 시도 (예: Asia/Seoul 직접 입력)
        if not timezone:
            timezone = location.strip()

        print(f"DEBUG: 위치 '{location}' -> 타임존 '{timezone}'")

        try:
            # Plan A: 외부 API (가끔 차단됨)
            url = f"http://worldtimeapi.org/api/timezone/{timezone}"
            resp = requests.get(url, timeout=2) # 타임아웃 2초로 단축
            resp.raise_for_status()
            dt = datetime.fromisoformat(resp.json()['datetime'])
            source = "API"
        except:
            # Plan B: Pytz 라이브러리 (무적의 자체 DB)
            try:
                tz = pytz.timezone(timezone)
                dt = datetime.now(tz)
                source = "내장 Pytz"
            except Exception as e:
                print(f"ERROR: 시간 조회 완전 실패 - {e}")
                return f"죄송합니다. '{location}'의 시간 정보를 찾을 수 없습니다."

        formatted_time = dt.strftime('%H시 %M분')
        print(f"SUCCESS: ({source}) {formatted_time}")
        
        return f"{location}의 현재 시간은 {formatted_time}입니다."