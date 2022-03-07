from rest_framework import serializers
from .models import Weather_data

class Weather_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather_data
        fields = ('id', 'road_station_id', 'sensor_id', 'sensor_value', 'measured_time')

class Create_Weather_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather_data
        fields = ('id', 'road_station_id', 'sensor_id', 'sensor_value', 'measured_time') 
