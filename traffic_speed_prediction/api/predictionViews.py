from django.db.migrations import serializer
from django.shortcuts import render
from rest_framework import generics, status
from .serializers import PredictionRequestSerializer, PredictionResponseSerializer
from .models import PredictionRequest, PredictionResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


class GetPredictionWithRoadId(APIView):
    serializer_class = PredictionRequestSerializer

    def get(self, request, roadId=None):
        predictedSpeed = 33.7  # predictedSpeed = AutoML.makePrediction(roadId)
        speedLimit = 50  # speedLimit = database.getSpeedLimitFor(roadId)
        prediction = PredictionResponse(roadId=roadId, onGoingSectionId=None, offGoingSectionId=None, speedLimit=speedLimit, predictedSpeed=predictedSpeed)
        prediction.save()
        data = PredictionResponseSerializer(prediction).data
        return Response(data, status=status.HTTP_200_OK)


class GetPredictionWithRoadIdAndSections(APIView):
    serializer_class = PredictionRequestSerializer

    def get(self, request, roadId=None, onGoing=None, offGoing=None):
        predictedSpeed = 33.7  # predictedSpeed = AutoML.makePrediction(roadId)
        speedLimit = 50  # speedLimit = database.getSpeedLimitFor(roadId)
        prediction = PredictionResponse(roadId=roadId, onGoingSectionId=onGoing, offGoingSectionId=offGoing, speedLimit=speedLimit, predictedSpeed=predictedSpeed)
        prediction.save()
        data = PredictionResponseSerializer(prediction).data
        return Response(data, status=status.HTTP_200_OK)








