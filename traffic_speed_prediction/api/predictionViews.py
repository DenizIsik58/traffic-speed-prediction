from rest_framework import generics, status
from .serializers import PredictionResponseSerializer
from .models import PredictionResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from util.db.database_commands import DatabaseCommands
from traffic_speed_prediction.auto_ml import auto_ml


class GetPrediction(APIView):
    serializer_class = PredictionResponseSerializer

    def get(self, request, lat=None, lon=None):
        auto_ml.train()
        dataToPredict = DatabaseCommands.getInfoForPredictionByLatAndLon(float(lat), float(lon))
        predictedSpeed = auto_ml.predict(dataToPredict)
        prediction = PredictionResponse(roadId=dataToPredict[0], predictedSpeed=predictedSpeed)
        prediction.save()
        data = PredictionResponseSerializer(prediction).data
        return Response(data, status=status.HTTP_200_OK)
    

class GetGeoJson(APIView):
    def get(self, request, roadNumber, roadSectionId):
        geodata = DatabaseCommands.getGeoJsonForRoadSection(roadNumber, roadSectionId)
        if(geodata is None): 
            return Response(geodata, status=status.HTTP_404_NOT_FOUND)
        return Response(geodata, status=status.HTTP_200_OK)




