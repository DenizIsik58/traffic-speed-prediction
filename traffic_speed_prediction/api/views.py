from http.client import HTTP_PORT
from django.shortcuts import render
from django.http import HttpResponse
import traffic_speed_prediction.model

from .serializers import RoadSectionSerializer
from rest_framework import viewsets
from .models import Road_section


# Create your views here.
def main(request):
    return HttpResponse("<h1>Hello World!</h1>")

class HeroViewSet(viewsets.ModelViewSet):
    queryset = Road_section.objects.all().order_by('road')
    serializer_class = RoadSectionSerializer

