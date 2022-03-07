from django.db import models


# Create your models here.
class Weather_data(models.Model):
    road_station_id = models.CharField(max_length=4, default="", unique=False)
    sensor_id = models.CharField(max_length=3, default="", unique=False)
    sensor_value = models.CharField(max_length=5, default="0.0", unique=False)
    measured_time = models.CharField(max_length=20, default="", unique=False)


