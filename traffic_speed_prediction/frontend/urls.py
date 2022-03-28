from django.urls import path
from .views import aboutUs, index, finmap, apiSite, itu, solita

urlpatterns = [
    path('', finmap, name="index"),
    path('finmap/', finmap, name="home"),
    path('apis/', apiSite, name="apis"),
    path('solita/', solita, name="solita"),
    path('itu/', itu, name="itu"),
    path('about/', aboutUs, name="aboutUs"),
]
