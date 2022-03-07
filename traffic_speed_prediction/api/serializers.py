from rest_framework import serializers
from .models import WeatherHistoryData

class WeatherHistoryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherHistoryData
        fields = ('id', 'roadStationId', 'sensorId', 'sensorValue', 'measuredTime')

class CreateWeatherHistoryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherHistoryData
        fields = ('id', 'roadStation_id', 'sensorId', 'sensorValue', 'measuredTime')
        
class UpdateWeatherHistoryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherHistoryData
        fields = ('id', 'roadStation_id', 'sensorId', 'sensorValue', 'measuredTime')
