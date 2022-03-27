from rest_framework import serializers

from .models import Road_section

class RoadSectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Road_section
        fields = ('road_section_number', 'road', 'roadTemperature', 'daylight', 'weatherSymbol', 'roadMaintenanceClass', 'freeFlowSpeed1', 'average_speed')