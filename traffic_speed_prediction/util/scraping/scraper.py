import string
import time

import requests
import ujson

from util.config.ReadConfig import Config

from api.models import Road


class Scraper:

    # Fetch data from any given endpoint
    @staticmethod
    def get_text_from_endpoint(path: string):
        return requests.get(path).text

    @staticmethod
    def fetch_and_create_db_object_from_tms_station_data():
        pass


    @staticmethod
    def get_road_ids():

        # Find all the ids related to road stations and road number
        for road_condition in ujson.loads(requests.get(Config.read_config()["urls"]["road_sections"]["base_url"]).text)[
            'weatherData']:
            road_number = str(road_condition["id"]).split("_")[0]
            road_sections = []
            # Find all the roadstation ids and road numbers
            for feature in \
            ujson.loads(requests.get(Config.read_config()["urls"]["road_number"]["base_url"] + road_number).text)[
                "features"]:
                road_sections.append(feature["properties"]["roadAddress"]["roadSection"])
            print("THESE IDS ARE BOUND TO ROAD NUMBER " + road_number)
            print(road_sections)
            Road(id=road_number, roadSections=road_sections).save()
            print("SAVING ROAD TO DB")

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



