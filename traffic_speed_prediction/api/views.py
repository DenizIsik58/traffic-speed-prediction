from django.db.migrations import serializer
from django.shortcuts import render
from rest_framework import generics, status
from .serializers import Weather_dataSerializer,Create_Weather_dataSerializer
from .models import Weather_data
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


class Weather_dataView(generics.ListAPIView):
    queryset = Weather_data.objects.all()
    serializer_class = Weather_dataSerializer


class GetWeather_data(APIView):
    serializer_class = Weather_dataSerializer
    lookup_url_kwarg = 'road_station_id'

    def get(self, request):
        road_station_id = request.GET.get(self.lookup_url_kwarg)
        if road_station_id is not None:
            weather_data = Weather_data.objects.filter(road_station_id=road_station_id)
            if len(weather_data) > 0:
                data = Weather_dataSerializer(weather_data[0]).data
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Weather station not found': 'Invalid weather station id.'},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'road_station_id not found in request'}, status=status.HTTP_404_NOT_FOUND)


class CreateWeather_data(APIView):
    serializer_class = Create_Weather_dataSerializer
    def post(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            road_station_id = serializer.data.get('road_station_id')
            sensor_id = serializer.data.get('sensor_id')
            sensor_value = serializer.data.get('sensor_value')
            measured_time = serializer.data.get('measured_time')
            queryset = Weather_data.objects.filter(road_station_id = road_station_id)
            if queryset.exists():
                weather_data = queryset[0]
                weather_data.road_station_id = road_station_id
                weather_data.sensor_id = sensor_id
                weather_data.sensor_value = sensor_value
                weather_data.measured_time = measured_time
                weather_data.save(update_fields=['road_station_id, sensor_id', 'sensor_value', 'measured_time'])
            else:
                weather_data = Weather_data(road_station_id=road_station_id, sensor_id=sensor_id,
                                            sensor_value=sensor_value, measured_time=measured_time)
                weather_data.save()

            return Response(Weather_dataSerializer(weather_data).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)



