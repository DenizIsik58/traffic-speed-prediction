import string
import time
import traceback

import requests
import ujson

from traffic_speed_prediction.util.config.ReadConfig import Config

from traffic_speed_prediction.api.models import Road, Road_section, TMS_station
from traffic_speed_prediction.util.data_cleaning.cleaner import *
from traffic_speed_prediction.util.data_cleaning.cleaner_conditions import *


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
        print("begin scraping")
        for road_condition in ujson.loads(requests.get(Config.read_config()["urls"]["road_sections"]["base_url"]).text)['weatherData']:
            # Check if this is the start of the roadsection, only part concerning us
            cleaned_road_condition = clean_and_repair([road_condition], conditions_for_roadConditions)
            if str(road_condition["id"]).split("_")[2] != "00000":
                continue
            road_temp = road_condition["roadConditions"][0]["roadTemperature"]
            daylight = road_condition["roadConditions"][0]["daylight"]
            weather_symbol = road_condition["roadConditions"][0]["weatherSymbol"]
            road_number = str(road_condition["id"]).split("_")[0]
            road_sections = []
            road_maintenance_classes = []
            free_flow_speed1s = []
            road_station_ids = []

            # Save road to database

            road = Road(Road_number=road_number)
            road.save()

            # Find all the roadstation ids and road numbers
            for feature in \
                    ujson.loads(
                        requests.get(Config.read_config()["urls"]["road_number"]["base_url"] + road_number).text)[
                        "features"]:

                # not all roads have maintanence classes. In this case set it to 0.
                try:
                    main = clean_and_repair([feature], conditions_for_roadNumber)
                    road_sections.append(main[0]["properties"]["roadAddress"]["roadSection"])
                    road_maintenance_classes.append(main[0]["properties"]["roadAddress"]["roadMaintenanceClass"])
                    free_flow_speed1s.append(main[0]["properties"]["freeFlowSpeed1"])
                    road_station_ids.append(main[0]["properties"]["roadStationId"])
                    print(str([main[0]["properties"]["roadAddress"]["roadSection"]][0]))
                    print("ROAD SECTION: " + str(main[0]["properties"]["roadAddress"]["roadSection"]))
                    print("FREE FLOW SPEED: " + str(main[0]["properties"]["freeFlowSpeed1"]))
                    print("ROAD STATION ID : " + str(main[0]["properties"]["roadStationId"]))
                except:
                    traceback.print_exc()
                    break
            i = -1
            for section in road_sections:

                i += 1
                if len(road_sections) == 0:
                    break
                for station in ujson.loads(requests.get(
                        Config.read_config()["urls"]["tms_station"]["base_url"] + str(road_station_ids[i])).text)[
                    "tmsStations"]:
                    cleaned_station = clean_and_repair([station], conditions_for_tmsData)
                    for censor in cleaned_station[0]["sensorValues"]:
                        if str(censor["id"]) == "5122":
                            avg_speed = censor["sensorValue"]
                            sect = Road_section(road_section_number=section, road=road, roadTemperature=road_temp,
                                        daylight=daylight,
                                        weatherSymbol=weather_symbol, roadMaintenanceClass=road_maintenance_classes[i],
                                        freeFlowSpeed1=free_flow_speed1s[i],
                                        average_speed=avg_speed)
                            sect.save()
                            TMS_station(tms_station=road_station_ids[i], roadSection=sect).save()
                            break
