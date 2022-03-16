from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.


class Road(models.Model):
    id = models.IntegerField(primary_key=True)
    roadSections = ArrayField(ArrayField(models.IntegerField()))


class Road_section(models.Model):
    id = models.IntegerField(primary_key=True)
    road = models.ForeignKey('Road', on_delete=models.CASCADE)
    roadTemperature = models.TextField()
    daylight = models.BooleanField()
    weatherSymbol = models.TextField()
    overallRoadCondition = models.TextField()


class TMS_station(models.Model):
    id = models.IntegerField(primary_key=True)
    road = models.ForeignKey('Road', on_delete=models.CASCADE)
    roadSection = models.ForeignKey('Road_section', on_delete=models.CASCADE)
