import csv
import json
import boto3
from util.config.ReadConfig import Config
from util.scraping.scraper import Scraper
from api.models import Road, Road_section, TMS_station

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
        Scraper.get_road_ids()



    @staticmethod
    def extract_data_and_write_to_csv():
        with open("BigData.csv", "w") as file:
            csv_writer = csv.writer(file)

            header = ['road_number', 'road_temperature', 'daylight', 'weather_symbol', 'roadMaintenanceClass', 'freeflowspeed', 'average_speed']
            csv_writer.writerow(header)
            for road_section in Road_section.objects.all():
                data = []
                data.append(road_section.road.Road_number)
                data.append(str(road_section.roadTemperature).replace("+", ""))
                data.append(int(road_section.daylight))
                data.append(str(str(road_section.weatherSymbol)[1:]))
                data.append(road_section.roadMaintenanceClass)
                data.append( road_section.freeFlowSpeed1)
                data.append(road_section.average_speed)
                csv_writer.writerow(data)

            file.close()

