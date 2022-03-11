from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.
class WeatherHistoryData(models.Model):
    roadStationId = models.IntegerField(default=0, unique=False)
    sensorId = models.IntegerField(default=0, unique=False)
    sensorValue = models.DecimalField(max_digits=4, decimal_places=1, default=0.0, unique=False)
    measuredTime = models.CharField(max_length=20, default="", unique=False)


class Road(models.Model):
    id = models.IntegerField(primary_key=True)
    road_sections = ArrayField(ArrayField(models.IntegerField()))


class Road_section(models.Model):
    id = models.IntegerField(primary_key=True)
    road = models.ForeignKey('Road', on_delete=models.CASCADE)
    road_temperature = models.TextField()
    day_light = models.BooleanField()
    road_condition = models.TextField()
    weather_symbol = models.TextField()
    overall_road_condition = models.TextField()


class TMS_station(models.Model):
    id = models.IntegerField(primary_key=True)
    road_number = models.ForeignKey('Road', on_delete=models.CASCADE)
    road_section = models.ForeignKey('Road_section', on_delete=models.CASCADE)
