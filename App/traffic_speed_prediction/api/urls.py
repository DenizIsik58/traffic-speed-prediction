#This class contains the urls with the paths to the API endpoints

from .predictionViews import *
from django.urls import include, path

urlpatterns = [
    path('get-pred&lat=<str:lat>&lon=<str:lon>&existingRoads=<str:existingRoads>', GetPrediction.as_view()),
    path('train-model', ModelTrainer.as_view()),
    path('get-geojson&roadNumber=<str:roadNumber>&roadSectionId=<str:roadSectionId>', GetGeoJson.as_view()),
    path('get-geojsonforallroadsections', GetGeoJsonForAllRoadSections.as_view()),
    path('update-geojsonforallroadsections', UpdateGeoJsonForAllRoadSections.as_view()),
    path('read-geojsonforallroadsections', ReadGeoJsonForAllRoadSections.as_view())

]
