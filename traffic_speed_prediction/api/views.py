from http.client import HTTP_PORT
from django.shortcuts import render
from django.http import HttpResponse
import traffic_speed_prediction.traffic_speed_prediction.model


# Create your views here.
def main(request):
    return HttpResponse("<h1>Hello World!</h1>")

def predict(request):
    return HttpResponse()

