from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.


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
