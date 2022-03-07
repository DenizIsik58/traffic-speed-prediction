from django.urls import path
from .views import Weather_dataView, GetWeather_data, CreateWeather_data

urlpatterns = [
    path('weather_data', Weather_dataView.as_view()),
    path('create-weather_data', CreateWeather_data.as_view()),
    path('get-weather_data/<int:road_station_id>/', GetWeather_data.as_view())
]
