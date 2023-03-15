from django.urls import path
from django.shortcuts import redirect
from .views import WeatherView


urlpatterns = [
    path("", lambda request: redirect("weather_page")),
    path("weather/", WeatherView.as_view(), name="weather_page")
]
