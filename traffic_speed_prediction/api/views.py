from django.db.migrations import serializer
from http.client import HTTP_PORT
from django.shortcuts import render
from rest_framework import generics, status
from .serializers import WeatherHistoryDataSerializer
from .models import WeatherHistoryData
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from.webscraper import tryGet
from .serializers import RoadSectionSerializer
from rest_framework import viewsets
from .models import Road_section


class WeatherHistoryDataView(generics.ListAPIView):
    queryset = WeatherHistoryData.objects.all()
    serializer_class = WeatherHistoryDataSerializer


class GetWeatherHistoryData(APIView):
    serializer_class = WeatherHistoryDataSerializer
    lookup_url_kwarg = 'roadStationId'

    def get(self, request):
        roadStationId = request.GET.get(self.lookup_url_kwarg)
        if roadStationId is not None:
            weatherHistoryData = WeatherHistoryData.objects.filter(roadStationId=roadStationId)
            if len(weatherHistoryData) > 0:
                data = WeatherHistoryDataSerializer(weatherHistoryData[0]).data
                return Response(data, status=status.HTTP_200_OK)
            return Response({'WeatherHistoryData not found': 'Invalid roadStationId.'},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'roadStationId not found in request'}, status=status.HTTP_404_NOT_FOUND)


class CreateWeatherHistoryData(APIView):
    serializer_class = WeatherHistoryDataSerializer

    def post(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            roadStationId = serializer.data.get('roadStationId')
            sensorId = serializer.data.get('sensorId')
            sensorValue = serializer.data.get('sensorValue')
            measuredTime = serializer.data.get('measuredTime')
            queryset = WeatherHistoryData.objects.filter(roadStationId = roadStationId)

            js = tryGet()
            print(js)
            for d in js:
                roadStationId = d['roadStationId']
                sensorId = d['sensorId']
                sensorValue = d['sensorValue']
                measuredTime = d['measuredTime']
                weatherHistoryData = WeatherHistoryData(roadStationId=roadStationId, sensorId=sensorId, sensorValue=sensorValue, measuredTime=measuredTime)
                weatherHistoryData.save()


            # if queryset.exists():
            #     weatherHistoryData = queryset[0]
            #     weatherHistoryData.roadStationId = roadStationId
            #     weatherHistoryData.sensorId = sensorId
            #     weatherHistoryData.sensorValue = sensorValue
            #     weatherHistoryData.measuredTime = measuredTime
            #     weatherHistoryData.save(update_fields=['roadStationId, sensorId', 'sensorValue', 'measuredTime'])
            # else:
            #     weatherHistoryData = WeatherHistoryData(roadStationId=roadStationId, sensorId=sensorId,
            #                                 sensorValue=sensorValue, measuredTime=measuredTime)
            #     weatherHistoryData.save()

            return Response(WeatherHistoryDataSerializer(weatherHistoryData).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateWeatherHistoryData(APIView):
    serializer_class = WeatherHistoryDataSerializer

    def put(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            roadStationId = serializer.data.get('roadStationId')
            sensorId = serializer.data.get('sensorId')
            sensorValue = serializer.data.get('sensorValue')
            measuredTime = serializer.data.get('measuredTime')
            queryset = WeatherHistoryData.objects.filter(roadStationId=roadStationId)
            if not queryset.exists():
                return Response({'msg': 'Station not found.'}, status=status.HTTP_404_NOT_FOUND)
            weatherHistoryData = queryset[0]
            weatherHistoryData.roadStationId = roadStationId
            weatherHistoryData.sensorId = sensorId
            weatherHistoryData.sensorValue = sensorValue
            weatherHistoryData.measuredTime = measuredTime
            weatherHistoryData.save(update_fields=['sensorId', 'sensorValue', 'measuredTime'])
            return Response(WeatherHistoryDataSerializer(weatherHistoryData).data, status=status.HTTP_200_OK)

        return Response({'Bad Request': "Invalid Data..."}, status=status.HTTP_400_BAD_REQUEST)


class DeleteWeatherHistoryData(APIView):
    def delete(self, request, pk):
        instance = WeatherHistoryData.objects.get(roadStationId=pk)
        instance.delete()
        return Response(WeatherHistoryDataSerializer.data, status=status.HTTP_200_OK)
class HeroViewSet(viewsets.ModelViewSet):
    queryset = Road_section.objects.all().order_by('road')
    serializer_class = RoadSectionSerializer

