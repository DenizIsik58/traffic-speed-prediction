from rest_framework import generics, status
from rest_framework.decorators import api_view

from rest_framework import generics, status
from util.scraping.scraper import Scraper
from .serializers import PredictionResponseSerializer
from .models import PredictionResponse, Road_section
from rest_framework.views import APIView
from rest_framework.response import Response
from util.db.database_commands import DatabaseCommands
from traffic_speed_prediction.auto_ml import auto_ml
import json

class GetPrediction(APIView):
    serializer_class = PredictionResponseSerializer

    global auto
    auto = auto_ml(False, False)

    # Existing roads are recieved as a string of format: x1, y1, x2, y2, x3, y3, ...
    def get(self, request, lat=None, lon=None, existingRoads=None):
        if auto_ml.isBeingTrained(auto):
            return Response({"message": "Model is currently being trained! Please wait!"},
                            status=status.HTTP_226_IM_USED)

        if not auto_ml.isTrained(auto):
            return Response({"message": "Model has not been trained yet!"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            dataToPredict = DatabaseCommands.getInfoForPredictionByLatAndLon(float(lat), float(lon), str(existingRoads))
        except:
            return Response({"message" : "Something went wrong fetching the road information. There might be road maintenance"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        predictedSpeed = auto_ml.predict(dataToPredict)
        prediction = PredictionResponse(roadId=dataToPredict[0], roadSectionId=dataToPredict[6],
                                        roadName=dataToPredict[7], predictedSpeed=predictedSpeed,
                                        selectedRoads=existingRoads)
        prediction.save()
        data = PredictionResponseSerializer(prediction).data
        return Response(data, status=status.HTTP_200_OK)


class ModelTrainer(APIView):

    def get(self, request):

        if auto_ml.isTrained(auto):
            return Response({"message": "model has already been trained"}, status=status.HTTP_400_BAD_REQUEST)

        if auto_ml.isBeingTrained(auto) or auto_ml.isTrained(auto):
            return Response({"message": "model is being trained right now. Please wait."}, status=status.HTTP_400_BAD_REQUEST)

        if not auto_ml.isBeingTrained(auto) or not auto_ml.isTrained(auto):
            auto_ml.train(auto)
            return Response({"message": "model is being trained right now"}, status=status.HTTP_400_BAD_REQUEST)




class GetGeoJson(APIView):
    def get(self, request, roadNumber, roadSectionId):
        geodata = Scraper.getGeoJsonForRoadSection(roadNumber, roadSectionId)
        # geodata is only none if the road section couldn't be found for the roadNumber
        if geodata is None:
            return Response(geodata, status=status.HTTP_404_NOT_FOUND)
        return Response(geodata, status=status.HTTP_200_OK)

class GetGeoJsonForAllRoadSections(APIView):
    def get(self, request):
        # This method takes geo data from Scraper.get_geo_data_for_all_road_sections() and adds it to a list if the corresponding road section exists in the database
        all_road_section_geo_data_in_db = Scraper.get_all_road_sections_geodata_in_db()
        if len(all_road_section_geo_data_in_db) > 0:
            return Response(all_road_section_geo_data_in_db, status=status.HTTP_200_OK)
        else:
            return Response(all_road_section_geo_data_in_db, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateGeoJsonForAllRoadSections(APIView):
    def get(self, request):
        all_road_section_geo_data_in_db = Scraper.update_all_road_sections_json()
        if len(all_road_section_geo_data_in_db) > 0:
            return Response(all_road_section_geo_data_in_db, status=status.HTTP_200_OK)
        else:
            return Response(all_road_section_geo_data_in_db, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReadGeoJsonForAllRoadSections(APIView):
    def get(self, request):
        with open("traffic_speed_prediction/all_road_sections_geodata.json", "r") as openfile:
            return Response(json.load(openfile),  status=status.HTTP_200_OK)
    
        

