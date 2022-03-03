import json
import boto3
from traffic_speed_prediction.util.config.ReadConfig import Config


class DatabaseCommands:
    # TODO: Make a class with commands for the DB

    # Put item in table
    @staticmethod
    def insert_to_database(object: json):
        # global keyword can be used here to look for variables out of scope
        resource_db = boto3.resource(
            service_name='dynamodb',
            aws_access_key_id=Config.read_secrets()["aws_access_key_id"],
            aws_secret_access_key=Config.read_secrets()["aws_secret_access_key"],
            region_name=Config.read_secrets()["region_name"]
        )

        # Dynamodb table
        table = resource_db.Table(Config.read_secrets()["table_name"])

        table.put_item(
            # Data to be inserted
            Item={
                'id': object["id"],
                'roadstation_id' : object["roadStationId"],
                'average_speed': object["sensorValue"],
                'date': object["date"],
                'time': object["time"],
            }
        )
