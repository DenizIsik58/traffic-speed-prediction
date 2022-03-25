from django.urls import path
from .views import index, home

urlpatterns = [
    path('', index, name="index"),
    path('home/', home, name="home"),
]
