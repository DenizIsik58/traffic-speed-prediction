from django.urls import path
from .views import *

urlpatterns = [
    path('', finmap, name="index"),
    path('finmap/', finmap, name="home"),
    path('apis/', apiSite, name="apis"),
    path('solita/', solita, name="solita"),
    path('itu/', itu, name="itu"),
    path('about/', aboutUs, name="aboutUs"),
    path('predictions/', predictions, name="predictions"),
]
