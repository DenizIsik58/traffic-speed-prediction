import ujson
import string
import requests
import time
from trafic_speed import Config
from traffic_speed_prediction.model.Dataobject import Dataobject


class Scraper:
    # TODO: Make a scraper class with static methods

    # Fetch data from any given endpoint
    @staticmethod
    def get_text_from_endpoint(path: string):
        return requests.get(path).text

    @staticmethod
    def fetch_and_create_db_object_from_tms_station_data():
        objects = []
        # Runs through the specified id's in the data.json file and fetches all the data
        # Then creates a Dataobject 0
        for station_id in Config.read_config()["urls"]["tms_station"]["ids"]:
            # Use ujson (written in C) library to increase performance
            data = ujson.loads(requests.get(Config.read_config()["urls"]["tms_station"]["base_url"] + station_id).text)
            for item in data['tmsStations'][0]['sensorValues']:
                if item["sensorUnit"] == "km/h":
                    object_id = item["id"]
                    roadstation_id = item["roadStationId"]
                    station_name = Config.read_config()["urls"]["tms_station"]["ids"][station_id]
                    speed = item["sensorValue"]
                    date = Config.convert_to_date(item["measuredTime"])[0]
                    time = Config.convert_to_date(item["measuredTime"])[1]
                    data_object = Dataobject(object_id, roadstation_id, station_name, speed, date, time)
                    objects.append(data_object)
        # Returns a list of Dataobjects
        return objects
    
    @staticmethod
    def get_road_ids():
        objects = []
        data = Scraper.get_text_from_endpoint(Config.read_config()["urls"]["road_sections"]["base_url"])
        for item in data["weatherData"] :
            objects.append(item["id"])
            print(item["id"])
        return objects
    

    @staticmethod
    def repeat_fetching(minutes: int):
        timer = time.time()
        minutes = minutes * 60
        counter = 0
        while True:
            counter += 1
            print("CURRENT BATCH: " + str(counter) + " DATA = ")
            for item in Scraper.fetch_and_create_db_object_from_tms_station_data():
                print(item)
            time.sleep(minutes - ((time.time() - timer) % minutes))

# Test code
if __name__ == '__main__':
    Scraper.get_road_ids
