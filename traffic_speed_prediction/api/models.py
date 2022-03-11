from django.db import models


# Create your models here.
class WeatherHistoryData(models.Model):
    roadStationId = models.IntegerField(default=0, unique=False)
    sensorId = models.IntegerField(default=0, unique=False)
    sensorValue = models.DecimalField(max_digits=4, decimal_places=1, default=0.0, unique=False)
    measuredTime = models.CharField(max_length=20, default="", unique=False)


