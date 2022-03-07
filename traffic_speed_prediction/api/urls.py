from django.urls import path
from .views import WeatherHistoryDataView, GetWeatherHistoryData, CreateWeatherHistoryData,UpdateWeatherHistoryData

urlpatterns = [
    path('all-whd', WeatherHistoryDataView.as_view()),
    path('create-whd', CreateWeatherHistoryData.as_view()),
    path('get-whd', GetWeatherHistoryData.as_view()),
    path('put-whd',UpdateWeatherHistoryData.as_view())
]
