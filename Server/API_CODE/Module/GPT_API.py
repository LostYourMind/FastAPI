# GPT_API.py
# GPT API를 활용한 코드들

import openai
import sys
import io
import os
from .weather_API import Weather
from datetime import datetime
import pytz

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


class USE_GPT:
    api_key = os.environ.get("")
    openai.api_key = api_key

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

    def generate_chat(prompt):
        """
        챗 모델을 이용한 텍스트 생성 함수.

        :param prompt: 모델에게 전달할 프롬프트.
        :param model: 사용할 모델의 이름.
        :param temperature: 생성된 텍스트의 창의성을 결정하는 온도 매개변수.
        :param max_tokens: 생성할 토큰(단어)의 최대 수.
        :return: 생성된 텍스트.
        """
        model = "gpt-3.5-turbo"
        temperature = 0.7
        max_tokens = 300

        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message["content"].strip()

    # GPT 호출
    def generate_Sentences(self, prompt):
        try:
            generated_text = USE_GPT.generate_chat(prompt)
            return generated_text
        except Exception as ex:
            print("오류 발생 :", ex)

    # 매뉴 추천 함수
    def Recomm_Menu(self, allergy, products):

        # 현재 위치 날씨 데이터 Dict 타입으로 정의
        celsius, condition = Weather.weather_info()
        current_time = USE_GPT.Time_Z()
        # #메뉴 추천 프롬프트
        prompt = f"메뉴 추천 부탁할께, 메뉴는 {products} 가 있고 현재 날씨는 {celsius}°C,{condition}이고, 현재 시간은{current_time}이야, {allergy}가 있어"
        try:
            generated_text = USE_GPT.generate_chat(prompt)
            return generated_text
        except Exception as ex:
            print("오류 발생 : ", ex)

    # Time_Zone 함수
    def Time_Z():
        seoul_tz = pytz.timezone("Asia/Seoul")
        current_time_seoul = datetime.now(seoul_tz)

        hours = current_time_seoul.hour
        minutes = current_time_seoul.minute
        seconds = current_time_seoul.second
        temp = f"{hours}:{minutes}:{seconds}"
        return temp
