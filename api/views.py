import requests
import redis
import json
from root import settings
from root.settings import APPID_KEY
from rest_framework.views import APIView
from rest_framework.response import Response


redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


class WeatherViev(APIView):
    def get(self, request, **kwargs):
        redis_sity = redis_instance.get(kwargs["city"])
        if not redis_sity:
            weather_data = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={kwargs['city']},&lang=ru&appid={APPID_KEY}&units=metric"
                ).json()
            if weather_data["cod"] == 200:
                response = {
                    "message": {
                            "city": weather_data["name"],
                            "temp": weather_data["main"]["temp"],
                            "description": weather_data["weather"][0]["description"],
                            "pressure": weather_data["main"]["pressure"],
                            "humidity": weather_data["main"]["humidity"],
                            "wind": weather_data["wind"]["speed"]
                        }
                }
                redis_instance.set(kwargs["city"], json.dumps(response).encode("utf-8"), ex=1800)
                return Response(response, status=200)
            else:
                return Response({"message": weather_data["message"]}, status=weather_data["cod"])
        else:
            response = json.loads(redis_sity.decode("utf-8"))
            return Response(response, status=200)


        