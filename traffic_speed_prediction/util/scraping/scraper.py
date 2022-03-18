import string
import time

import requests
import ujson

from util.config.ReadConfig import Config

from api.models import Road, Road_section, TMS_station


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
        global road_station_id, road_maintenance_class, free_flow_speed1, avg_speed
        for road_condition in ujson.loads(requests.get(Config.read_config()["urls"]["road_sections"]["base_url"]).text)[
            'weatherData']:
            road_temp = road_condition["roadConditions"][0]["roadTemperature"]
            daylight = road_condition["roadConditions"][0]["daylight"]
            weather_symbol = road_condition["roadConditions"][0]["weatherSymbol"]

            road_number = str(road_condition["id"]).split("_")[0]
            road_sections = []

            road = Road(Road_number=road_number)
            road.save()
            # Find all the roadstation ids and road numbers
            for feature in \
                    ujson.loads(
                        requests.get(Config.read_config()["urls"]["road_number"]["base_url"] + road_number).text)[
                        "features"]:
                road_sections.append(feature["properties"]["roadAddress"]["roadSection"])
                road_maintenance_class = feature["properties"]["roadAddress"]["roadMaintenanceClass"]
                free_flow_speed1 = feature["properties"]["freeFlowSpeed1"]
                road_station_id = feature["properties"]["roadStationId"]
            print("THESE IDS ARE BOUND TO ROAD NUMBER " + road_number)
            print(road_number)
            print(road_sections)
            for section in road_sections:
                if len(road_sections) == 0:
                    break
                for station in ujson.loads(requests.get(
                        Config.read_config()["urls"]["tms_station"]["base_url"] + str(road_station_id)).text)[
                    "tmsStations"]:
                    for censor in station["sensorValues"]:
                        if censor["id"] == str(5122):
                            avg_speed = station["sensorValue"]
                            print("AVG SPEED: " + avg_speed)
                            Road_section(road_section_number=section, road=road, roadTemperature=road_temp,
                                         daylight=daylight,
                                         weatherSymbol=weather_symbol, roadMaintenanceClass=road_maintenance_class,
                                         freeFlowSpeed1=free_flow_speed1,
                                         average_speed=avg_speed).save()
                            TMS_station(tms_station=road_station_id, roadSection=section).save()
                            print("SAVING ROAD TO DB")
                            break



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
