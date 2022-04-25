from rest_framework import serializers
from .models import *
from .models import Road_section


class WeatherHistoryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherHistoryData
        fields = ('id', 'roadStationId', 'sensorId', 'sensorValue', 'measuredTime')

        
class PredictionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionResponse
        fields = ('id', 'roadId', 'roadName', 'roadSectionId','predictedSpeed', 'selectedRoads')


class RoadSectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Road_section
        fields = ('road_section_number', 'road', 'roadTemperature', 'daylight', 'weatherSymbol', 'roadMaintenanceClass', 'freeFlowSpeed1', 'average_speed', 'roadName')
