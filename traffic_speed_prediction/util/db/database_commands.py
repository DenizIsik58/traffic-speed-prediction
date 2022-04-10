import csv
import json
import requests
import ujson
import boto3
from util.config.ReadConfig import Config
from util.scraping.scraper import Scraper
from api.models import Road, Road_section, TMS_station
import math
from traffic_speed_prediction.auto_ml import auto_ml


class DatabaseCommands:

    @staticmethod
    def load_database():
        Scraper.load_data()

    @staticmethod
    def extract_data_and_write_to_csv():
        with open("BigData.csv", "w") as file:
            csv_writer = csv.writer(file)

            header = ['road_number', 'road_temperature', 'daylight', 'weather_symbol', 'roadMaintenanceClass',
                      'freeflowspeed', 'average_speed']
            csv_writer.writerow(header)
            for road_section in Road_section.objects.all():
                data = []
                data.append(road_section.road.Road_number)
                data.append(float(str((road_section.roadTemperature).replace("+", ""))))
                data.append(int(road_section.daylight))
                data.append(str(road_section.weatherSymbol)[1:])
                data.append(road_section.roadMaintenanceClass)
                data.append(float((road_section.freeFlowSpeed1)))
                data.append(float((road_section.average_speed)))
                csv_writer.writerow(data)

            file.close()

    @staticmethod
    def getInfoForPredictionByLatAndLon(lon2, lat2):
        nearest_distance = 10000
        road_section_id = -1
        road_number = -1

        usingHaversine = False

        for road_section in Road_section.objects.all():
            lat1 = road_section.lat
            lon1 = road_section.lon

            deltaLon = lat1 - lat2
            deltaLat = lon1 - lon2
            
            if(usingHaversine):
                # Haversine distance between coordinaates
                dlon = lon2 - lon1
                dlat = lat2 - lat1 
                a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
                c = 2 * math.asin(math.sqrt(a)) 

                #6371 is in kilometers. Multiply with 1000 for meters
                temp_distance = c*6371
            else:
                #Using euclidean is faster, but not as accurtae. Works without problem on area as small as Finland
                temp_distance = math.sqrt(
                    deltaLon*deltaLon + deltaLat*deltaLat
                )

            if nearest_distance > temp_distance:
                road_section_id = road_section.road_section_number
                road_number = road_section.road.Road_number
            return (str(road_number), str(road_section_id))





