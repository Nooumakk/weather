from django.urls import path
from .views import WeatherViev


urlpatterns = [
    path("api/v1/weather/<str:city>", WeatherViev.as_view()),
]
