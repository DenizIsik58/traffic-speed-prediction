import json
import boto3
from traffic_speed_prediction.util.config.ReadConfig import Config


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
        print(table_name)
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




