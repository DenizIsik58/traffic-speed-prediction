from rest_framework import serializers
from .models import *

class WeatherHistoryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherHistoryData
        fields = ('id', 'roadStationId', 'sensorId', 'sensorValue', 'measuredTime')

class PredictionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionRequest
        fields = ('id', 'roadId', 'onGoingSectionId', 'offGoingSectionId')
        
class PredictionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionResponse
        fields = ('id', 'roadId', 'onGoingSectionId', 'offGoingSectionId', 'speedLimit', 'predictedSpeed')


