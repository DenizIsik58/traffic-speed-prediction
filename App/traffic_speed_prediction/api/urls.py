from django.urls import path
from .views import *
from .predictionViews import *

from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'heroes', views.HeroViewSet)

urlpatterns = [
    path('all-whd', WeatherHistoryDataView.as_view()),
    path('create-whd', CreateWeatherHistoryData.as_view()),
    path('get-whd', GetWeatherHistoryData.as_view()),
    path('put-whd', UpdateWeatherHistoryData.as_view()),
    path('delete-whd/<int:pk>/', DeleteWeatherHistoryData.as_view()),
    path('get-pred&lat=<str:lat>&lon=<str:lon>&existingRoads=<str:existingRoads>', GetPrediction.as_view()),
    path('train-model', ModelTrainer.as_view()),
    path('get-geojson&roadNumber=<str:roadNumber>&roadSectionId=<str:roadSectionId>', GetGeoJson.as_view()),
    path('get-geojsonforallroadsections', GetGeoJsonForAllRoadSections.as_view())

]
