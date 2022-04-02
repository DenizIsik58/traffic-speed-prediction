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
    def getNearestCoordsAndPredictions(lat, lon):

        nearest_distance = 10000
        road_sect = []
        la = 0
        lo = 0

        for road_section in Road_section.objects.all():
            temp_distance = math.sqrt(
                math.pow(road_section.lat - lat, 2) + math.pow(road_section.lon - lon, 2))
            if nearest_distance > temp_distance:
                la = road_section.lat
                lo = road_section.lon
                road_sect.clear()
                nearest_distance = temp_distance
                road_sect.append(road_section.road.Road_number)
                road_sect.append(float(str((road_section.roadTemperature).replace("+", ""))))
                road_sect.append(int(road_section.daylight))
                road_sect.append(int(str(road_section.weatherSymbol)[1:]))
                road_sect.append(int(road_section.roadMaintenanceClass))
                road_sect.append(float((road_section.freeFlowSpeed1)))
                print(road_section.road.Road_number)
        print(road_sect)
        print("NEAREST: " + str(nearest_distance))
        print("LAT: " + str(la) + " LON: " + str(lo))
        print("PREDICTIONS: " + str(auto_ml.predict(road_sect)))

    @staticmethod
    def getInfoForPredictionByLatAndLon(lon2, lat2):

        nearest_distance = 10000
        road_sect = []
        la = 0
        lo = 0

        r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.

        print("Query points:")
        print("Lat:", lat2)
        print("Lon:", lon2)

        for road_section in Road_section.objects.all():
            lat1 = road_section.lat
            lon1 = road_section.lon

            deltaLon = lat1 - lat2
            deltaLat = lon1 - lon2
            
            #Using euclidean is faster, but is super imprecise. always gets the same result
            temp_distance = math.sqrt(
                deltaLon*deltaLon+ deltaLat*deltaLat
            )

            #print("recieved lat:")
            #print(lat2)
            #print("recieved long")
            #print(lon2)

            # Haversine distance between coordinaates
            #dlon = lon2 - lon1 
            #dlat = lat2 - lat1 
            #a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            #c = 2 * math.asin(math.sqrt(a)) 

            #temp_distance=r*c

            #print(meters)
            if nearest_distance > temp_distance:
                print(temp_distance)
                la = road_section.lat
                lo = road_section.lon
                road_sect.clear()
                nearest_distance = temp_distance
                road_sect.append(road_section.road.Road_number)
                road_sect.append(float(str((road_section.roadTemperature).replace("+", ""))))
                road_sect.append(int(road_section.daylight))
                road_sect.append(int(str(road_section.weatherSymbol)[1:]))
                road_sect.append(int(road_section.roadMaintenanceClass))
                road_sect.append(float((road_section.freeFlowSpeed1)))
                road_sect.append(int((road_section.road_section_number)))
                print("found new closest road: ")
                print(road_section.road.Road_number, road_section.road_section_number)

        print("lat, long of closest road: ", la, lo)
        return road_sect
    

    # This doesn't really have anything to do with the database, should be moved
    # Possible improvement: Include ALL the geodata for the same road section. 
    # Right now we only take from the first part of the road section
    def getGeoJsonForRoadSection(roadNumber, roadSectionId):
        apiPath = "https://tie.digitraffic.fi/api/v2/metadata/forecast-sections/" + roadNumber;

        response = requests.get(apiPath).text

        # Iterate over evert road section in the recieved json
        for road_section in ujson.loads(response)["features"]:
            #print("Printing debug: " + str(road_section["id"]))

            #Get the total id, split it, and find just the road section id
            index_roadID = road_section["properties"]["id"];
            index_roadSectionId = index_roadID.split("_")[1]

            #print(index_roadID, index_roadSectionId)

            # If we find the correct road section, return its list of points
            if(int(index_roadSectionId) == int(roadSectionId)):
                return road_section["geometry"]["coordinates"]
        
        # If nothing is found, return none
        return None




