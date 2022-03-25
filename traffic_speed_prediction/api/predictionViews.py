from django.db.migrations import serializer
from django.shortcuts import render
from rest_framework import generics, status
from .serializers import PredictionRequestSerializer, PredictionResponseSerializer
from .models import PredictionRequest, PredictionResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

class GetPrediction(APIView):
    serializer_class = PredictionRequestSerializer
    lookup_url_kwarg = 'roadId'
    def get(self, request):
        roadId = request.GET.get(self.lookup_url_kwarg)
        predictionRequest = PredictionRequest.objects.filter(roadId = roadId)
        # predictedSpeed = AutoML.makePrediction(roadId)
        # speedLimit = database.getSpeedLimitfor(roadId)
        predictedSpeed = 33.7
        speedLimit = 50
        prediction = PredictionResponse(roadId=roadId, onGoingSectionId=None, offGoingSectionId=None, speedLimit=speedLimit, predictedSpeed=predictedSpeed)
        prediction.save()
        data = PredictionResponseSerializer(prediction).data
        return Response(data, status=status.HTTP_200_OK)








