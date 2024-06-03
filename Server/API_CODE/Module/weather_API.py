# weather_API.py
# 날씨 데이터 API를 사용한 코드들
import os
import sys
import requests


class Weather:

    def weather_info():

        api_key = os.environ.get("")
        LOCATION = "Your Location Name"

        # WeatherAPI 날씨 예보 정보 조회 URL (현재 + 오늘의 최고/최저 기온 포함)
        url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={LOCATION}&days=1&aqi=no"

        try:
            response = requests.get(url)
            weather_data = response.json()

            return (
                weather_data["current"]["temp_c"],
                weather_data["current"]["condition"]["text"],
            )

        except Exception as ex:
            print("오류 발생 : ", ex)
