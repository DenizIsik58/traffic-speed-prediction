from rest_framework import generics, status

from util.scraping.scraper import Scraper
from .serializers import PredictionResponseSerializer
from .models import PredictionResponse, Road_section
from rest_framework.views import APIView
from rest_framework.response import Response
from util.db.database_commands import DatabaseCommands
from traffic_speed_prediction.auto_ml import auto_ml


class GetPrediction(APIView):
    serializer_class = PredictionResponseSerializer

    def get(self, request, lat=None, lon=None):
        road_number, road_section = DatabaseCommands.getInfoForPredictionByLatAndLon(float(lat), float(lon))
        # Fetch live data and make prediction based on that
        data_to_predict = Scraper.get_live_road_section_info_by_id(road_number, road_section)
        predictedSpeed = auto_ml.predict(data_to_predict)
        prediction = PredictionResponse(roadId=data_to_predict[0], roadSectionId=road_section, predictedSpeed=predictedSpeed)
        prediction.save()
        data = PredictionResponseSerializer(prediction).data
        return Response(data, status=status.HTTP_200_OK)
    

class GetGeoJson(APIView):
    def get(self, request, roadNumber, roadSectionId):
        geodata = Scraper.getGeoJsonForRoadSection(roadNumber, roadSectionId)

        # geodata is only none if the road section couldn't be found for the roadNumber
        if(geodata is None): 
            return Response(geodata, status=status.HTTP_404_NOT_FOUND)
        
        return Response(geodata, status=status.HTTP_200_OK)




