import json
import string
import requests
from traffic_speed_prediction.util.config.ReadConfig import read_config, convert_to_date


# Fetch data from any given endpoint
def get_text_from_endpoint(path: string):
    return requests.get(path).text


# Fetch data of a tms station with a specific id
def get_tms_station_data(id: string):
    return json.loads(requests.get(read_config()["urls"]["tms_station"]["base_url"] + id).text)


def create_db_object(data: json):
    for item in data['tmsStations'][0]['sensorValues']:
        if item["sensorUnit"] == "km/h":
            object_id = item["id"]
            roadstation_id = item["roadStationId"]
            speed = item["sensorValue"]
            date = convert_to_date(item["measuredTime"])[0]
            time = convert_to_date(item["measuredTime"])[1]

            # Returns a json object
            # TODO: Make sure to return a list of objects we fetch from the api to insert into the DB
            return {"object_id": object_id, "roadStationId": roadstation_id, "sensorValue": speed, "date": date,
                    "time": time}


# Test code
if __name__ == '__main__':
    print(create_db_object(get_tms_station_data("23001")))
