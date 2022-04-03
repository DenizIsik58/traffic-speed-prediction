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
    # TODO: Make a class with commands for the DB

    # Put item in table
    def __init__(self):
        pass

    @staticmethod
    def insert_to_database(object: json, table_name: str):
        if table_name == "roads":
            table_name = Config.read_secrets()["secrets"]["table_names"]["road_table"]
        elif table_name == "tms":
            table_name = Config.read_secrets()["secrets"]["table_names"]["station_table"]
        # global keyword can be used here to look for variables out of scope
        resource_db = boto3.resource(
            service_name='dynamodb',
            aws_access_key_id=Config.read_secrets()["secrets"]["aws_access_key_id"],
            aws_secret_access_key=Config.read_secrets()["secrets"]["aws_secret_access_key"],
            region_name=Config.read_secrets()["secrets"]["region_name"]
        )

        # Dynamodb table
        table = resource_db.Table(table_name)
        table.put_item(
            # Data to be inserted
            Item={
                'Id': object["id"],
                'roadstation_id': object["roadStationId"],
                'average_speed': object["sensorValue"],
                'date': object["date"],
                'time': object["time"],
            }
        )

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
        road_sect = []

        usingHaversine = False;

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
                    deltaLon*deltaLon+ deltaLat*deltaLat
                )

            if nearest_distance > temp_distance:
                road_sect.clear()
                nearest_distance = temp_distance
                road_sect.append(road_section.road.Road_number)
                road_sect.append(float(str((road_section.roadTemperature).replace("+", ""))))
                road_sect.append(int(road_section.daylight))
                road_sect.append(int(str(road_section.weatherSymbol)[1:]))
                road_sect.append(int(road_section.roadMaintenanceClass))
                road_sect.append(float((road_section.freeFlowSpeed1)))
                road_sect.append(int((road_section.road_section_number)))

        return road_sect
    

    # This doesn't really have anything to do with the database, should be moved
    def getGeoJsonForRoadSection(roadNumber, roadSectionId):
        apiPath = "https://tie.digitraffic.fi/api/v2/metadata/forecast-sections/" + roadNumber;

        response = requests.get(apiPath).text
        allSectionsData = []

        # Iterate over evert road section in the recieved json
        for road_section in ujson.loads(response)["features"]:

            #Get the total id, split it, and find just the road section id
            index_roadID = road_section["properties"]["id"];
            index_roadSectionId = index_roadID.split("_")[1]

            # If we find the correct road section, return its list of points
            if(int(index_roadSectionId) == int(roadSectionId)):
                for element in road_section["geometry"]["coordinates"]:
                    allSectionsData.append(element)
        
        # If nothing is found, return none
        if(len(allSectionsData) > 0):
            return allSectionsData
        else:
             return None




