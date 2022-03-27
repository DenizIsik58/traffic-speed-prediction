from django.urls import path
from .views import main

from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'heroes', views.HeroViewSet)

urlpatterns = [
    path('', main),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
