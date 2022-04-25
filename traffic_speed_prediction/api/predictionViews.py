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

    #Existing roads are recieved as a string of format: x1, y1, x2, y2, x3, y3, ...
    def get(self, request, lat=None, lon=None, existingRoads=None):
        print(existingRoads)
        #auto_ml.train()
        dataToPredict = DatabaseCommands.getInfoForPredictionByLatAndLon(float(lat), float(lon), str(existingRoads))
        predictedSpeed = auto_ml.predict(dataToPredict)
        prediction = PredictionResponse(roadId=dataToPredict[0], roadSectionId=dataToPredict[6], roadName=dataToPredict[7], predictedSpeed=predictedSpeed, selectedRoads=existingRoads)
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





