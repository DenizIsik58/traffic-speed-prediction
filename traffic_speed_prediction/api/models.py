from django.contrib.postgres.fields import ArrayField
from django.db import models


class WeatherHistoryData(models.Model):
    roadStationId = models.IntegerField(default=0, unique=False)
    sensorId = models.IntegerField(default=0, unique=False)
    sensorValue = models.DecimalField(max_digits=4, decimal_places=1, default=0.0, unique=False)
    measuredTime = models.CharField(max_length=20, default="", unique=False)

class Road(models.Model):
    Road_number = models.IntegerField()


class Road_section(models.Model):
    road_section_number = models.IntegerField()
    road = models.ForeignKey('Road', on_delete=models.CASCADE)
    roadTemperature = models.TextField()
    lat = models.FloatField()
    lon = models.FloatField()
    daylight = models.BooleanField()
    weatherSymbol = models.TextField()
    roadMaintenanceClass = models.TextField()
    freeFlowSpeed1 = models.TextField()
    average_speed = models.FloatField()


class TMS_station(models.Model):
    tms_station = models.IntegerField()
    roadSection = models.ForeignKey('Road_section', on_delete=models.CASCADE)

class PredictionRequest(models.Model):
    roadId = models.IntegerField(default=0)
    onGoingSectionId = models.IntegerField(null=True, default=0)
    offGoingSectionId = models.IntegerField(null=True, default=0)

class PredictionResponse(models.Model):
    roadId = models.IntegerField(default=0)
    onGoingSectionId = models.IntegerField(null=True, default=0)
    offGoingSectionId = models.IntegerField(null=True, default=0)
    speedLimit = models.IntegerField(default=0)
    predictedSpeed = models.FloatField(default=0)







