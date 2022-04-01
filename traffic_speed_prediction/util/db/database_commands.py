import csv
import json
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
    def getInfoForPredictionByLatAndLon(lat2, lon2):

        nearest_distance = 10000
        road_sect = []
        la = 0
        lo = 0

        print("recieved lat:")
        print(lat2)
        print("recieved long")
        print(lon2)

        counter = 0;

        #for road_section in Road_section.objects.all():
          #  if(road_section.lat > 0 and road_section.lon > 0):
            #    counter = counter + 1

        print(counter)

        for road_section in Road_section.objects.all():
            lat1 = road_section.lat
            lon1 = road_section.lon
            
            #Using euclidean is faster, but is super imprecise. always gets the same result
            #temp_distance = math.sqrt(
            #    math.pow(lat1 - lat2, 2) + math.pow(lon1 - lon2, 2)
            #)

            #print("recieved lat:")
            #print(lat2)
            #print("recieved long")
            #print(lon2)

            # Haversine distance between coordinaates
            dlon = lon2 - lon1 
            dlat = lat2 - lat1 
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a)) 
            r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.

            temp_distance=r*c

            #print(meters)
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
                print("found new closest road: ")
                print(road_section.road.Road_number)
        return road_sect




