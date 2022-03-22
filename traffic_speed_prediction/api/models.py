from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.

class Road(models.Model):
    Road_number = models.IntegerField()


class Road_section(models.Model):
    road_section_number = models.IntegerField()
    road = models.ForeignKey('Road', on_delete=models.CASCADE)
    roadTemperature = models.TextField()
    daylight = models.BooleanField()
    weatherSymbol = models.TextField()
    roadMaintenanceClass = models.TextField()
    freeFlowSpeed1 = models.TextField()
    average_speed = models.FloatField()


class TMS_station(models.Model):
    tms_station = models.IntegerField()
    roadSection = models.ForeignKey('Road_section', on_delete=models.CASCADE)
