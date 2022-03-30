from django.urls import path
from .views import *
from .predictionViews import *

urlpatterns = [
    path('all-whd', WeatherHistoryDataView.as_view()),
    path('create-whd', CreateWeatherHistoryData.as_view()),
    path('get-whd', GetWeatherHistoryData.as_view()),
    path('put-whd', UpdateWeatherHistoryData.as_view()),
    path('delete-whd/<str:pk>/', DeleteWeatherHistoryData.as_view()),

    path('get-pred&roadId=<int:roadId>', GetPredictionWithRoadId.as_view()),
    path('get-pred&roadId=<int:roadId>&onGoing=<int:onGoing>&offGoing=<int:offGoing>', GetPredictionWithRoadIdAndSections.as_view())
]