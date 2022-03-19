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

        for road_condition in ujson.loads(requests.get(Config.read_config()["urls"]["road_sections"]["base_url"]).text)['weatherData']:
            road_temp = road_condition["roadConditions"][0]["roadTemperature"]
            daylight = road_condition["roadConditions"][0]["daylight"]
            weather_symbol = road_condition["roadConditions"][0]["weatherSymbol"]
            road_number = str(road_condition["id"]).split("_")[0]
            road_sections = []
            road_maintenance_classes = []
            free_flow_speed1s = []
            road_station_ids = []

            road = Road(Road_number=road_number)
            road.save()
            # Find all the roadstation ids and road numbers

            for feature in \
                    ujson.loads(
                        requests.get(Config.read_config()["urls"]["road_number"]["base_url"] + road_number).text)[
                        "features"]:
                road_sections.append(feature["properties"]["roadAddress"]["roadSection"])
                try:
                    road_maintenance_classes.append(feature["properties"]["roadAddress"]["roadMaintenanceClass"])
                except:
                    road_maintenance_classes.append(0)
                free_flow_speed1s.append(feature["properties"]["freeFlowSpeed1"])
                road_station_ids.append(feature["properties"]["roadStationId"])

            # print("THESE IDS ARE BOUND TO ROAD NUMBER " + road_number)
            i = -1
            for section in road_sections:

                i += 1
                if len(road_sections) == 0:
                    break
                for station in ujson.loads(requests.get(
                        Config.read_config()["urls"]["tms_station"]["base_url"] + str(road_station_ids[i])).text)[
                    "tmsStations"]:
                    for censor in station["sensorValues"]:
                        if str(censor["id"]) == "5122":
                            avg_speed = censor["sensorValue"]
                            print("road_section: " + str(
                                section) + " road number: " + road_number + " road station number " + str(
                                road_station_ids[i]))
                            print("--------------------")
                            print("AVG SPEED: " + str(avg_speed))
                            print("weather: " + weather_symbol)
                            print("daylight: " + str(daylight))
                            print("roadmain: " + str(road_maintenance_classes[i]))
                            print("Free flow speed: " + str(free_flow_speed1s[i]))
                            print("road temp: " + road_temp)
                            sect = Road_section(road_section_number=section, road=road, roadTemperature=road_temp,
                                        daylight=daylight,
                                        weatherSymbol=weather_symbol, roadMaintenanceClass=road_maintenance_classes[i],
                                        freeFlowSpeed1=free_flow_speed1s[i],
                                        average_speed=avg_speed)
                            sect.save()
                            TMS_station(tms_station=road_station_ids[i], roadSection=sect).save()
                            print("SAVING ROAD TO DB")
                            print()
                            print()
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
