import string
import traceback
import requests
import ujson

from util.config.ReadConfig import Config

from api.models import Road, Road_section, TMS_station
from util.data_cleaning.cleaner import *
from util.data_cleaning.cleaner_conditions import *
import json


class Scraper:

    # Fetch data from any given endpoint
    @staticmethod
    def get_text_from_endpoint(path: string):
        return requests.get(path).text

    @staticmethod
    def fetch_and_create_db_object_from_tms_station_data():
        pass

    # Get all known road sections from an API call
    # and then save them to the database
    @staticmethod
    def load_data():
        # Find all the ids related to road stations and road number
        for road_condition in ujson.loads(requests.get(Config.read_config()["urls"]["road_sections"]["base_url"]).text)[
            'weatherData']:
            # Check if this is the start of the roadsection, only part concerning us
            cleaned_road_condition = clean_and_repair([road_condition], conditions_for_roadConditions)

            if str(cleaned_road_condition[0]["id"]).split("_")[2] != "00000" and cleaned_road_condition[0][
                "roadConditions"] != []:
                continue

            daylight = cleaned_road_condition[0]["roadConditions"][1]["daylight"]
            road_temp = cleaned_road_condition[0]["roadConditions"][1]["roadTemperature"]
            weather_symbol = cleaned_road_condition[0]["roadConditions"][1]["weatherSymbol"]
            road_number = str(cleaned_road_condition[0]["id"]).split("_")[0]
            road_sections = []
            road_maintenance_classes = []
            free_flow_speed1s = []
            road_station_ids = []
            lat = []
            lon = []
            roadName = ""

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
                    lat.append(main[0]["geometry"]["coordinates"][0])
                    lon.append(main[0]["geometry"]["coordinates"][1])
                    roadName = str(main[0]["properties"]["names"]["fi"])
                    print(main[0]["properties"]["names"]["fi"])
                except:
                    traceback.print_exc()
                    break
            
            # Find all the road sections and save them to the database
            # A road section will have much data in common with its road 
            # (so all road sections of the same road will share some data)
            # Maybe this should be made into an index loop
            i = -1
            for section in road_sections:

                i += 1
                if len(road_sections) == 0:
                    break
                for station in ujson.loads(requests.get(
                        Config.read_config()["urls"]["tms_station"]["base_url"] + str(road_station_ids[i])).text)[
                    "tmsStations"]:

                    cleaned_station = clean_and_repair([station], conditions_for_tmsData)
                    try:
                        for censor in cleaned_station[0]["sensorValues"]:
                            if str(censor["id"]) == "5122":
                                avg_speed = censor["sensorValue"]
                                sect = Road_section(road_section_number=section, road=road, roadTemperature=road_temp,
                                                    lat=lat[i], lon=lon[i],
                                                    daylight=daylight,
                                                    weatherSymbol=weather_symbol,
                                                    roadMaintenanceClass=road_maintenance_classes[i],
                                                    freeFlowSpeed1=free_flow_speed1s[i],
                                                    average_speed=avg_speed,
                                                    roadName=roadName)
                                sect.save()
                                TMS_station(tms_station=road_station_ids[i], roadSection=sect).save()
                                break
                    except:
                        break

        # Update all_road_sections_geodata.json with new data
        Scraper.update_all_road_sections_json()



    @staticmethod
    def get_live_road_section_info_by_id(road_number, road_section_id):
        road_section = []

        for road_condition in \
        ujson.loads(requests.get(Config.read_config()["urls"]["road_sections"]["base_url"] + road_number).text)[
            'weatherData']:
            cleaned_road_condition = clean_and_repair([road_condition], conditions_for_roadConditions)

            if str(cleaned_road_condition[0]["id"]).split("_")[2] != "00000" and cleaned_road_condition[0][
                "roadConditions"] != []:
                continue
            road_section.append(int(str(cleaned_road_condition[0]["id"]).split("_")[0]))
            road_section.append(cleaned_road_condition[0]["roadConditions"][0]["roadTemperature"].replace("+", ""))  # road temperature

            road_section.append(int(cleaned_road_condition[0]["roadConditions"][0]["daylight"]))  # daylight
            road_section.append(str(cleaned_road_condition[0]["roadConditions"][0]["weatherSymbol"])[1:])  # weathersymbol
              # road_number
            break
        for feature in \
        ujson.loads(requests.get(Config.read_config()["urls"]["road_number"]["base_url"] + str(road_number)).text)[
            "features"]:
            try:
                main = clean_and_repair([feature], conditions_for_roadNumber)
                if str(main[0]['properties']['roadAddress']['roadSection']) == str(road_section_id):
                    road_section.append(main[0]["properties"]["roadAddress"]["roadMaintenanceClass"])
                    road_section.append(main[0]["properties"]["freeFlowSpeed1"])
                    return road_section
            except:
                traceback.print_exc()

    # Get geojson for a specific road id and road section id
    # The geojson contains the points which are needed to draw the road
    @staticmethod
    def getGeoJsonForRoadSection(roadNumber, roadSectionId):
        apiPath = "https://tie.digitraffic.fi/api/v2/metadata/forecast-sections/" + roadNumber

        response = requests.get(apiPath).text
        allSectionsData = []

        # Iterate over evert road section in the recieved json
        for road_section in ujson.loads(response)["features"]:

            # Get the total id, split it, and find just the road section id
            index_roadID = road_section["properties"]["id"]
            index_roadSectionId = index_roadID.split("_")[1]

            # If we find the correct road section, return its list of points
            # A road section can appear multiple times, as it is split into smaller segments
            # We ignore this, and just find the entire road section
            if int(index_roadSectionId) == int(roadSectionId):
                for element in road_section["geometry"]["coordinates"]:
                    allSectionsData.append(element)

        # If nothing is found, return none
        if len(allSectionsData) > 0:
            return allSectionsData
        else:
            return None



    @staticmethod
    def get_geodata_for_all_road_sections():
        api_path = "https://tie.digitraffic.fi/api/v2/metadata/forecast-sections/"
        response = requests.get(api_path).text
        all_road_sections = [] # list of (geo data, road id, road section id)

        # Add the geo data of all road sections to all_road_sections as a tuple containing the geo data, road id and road section id
        for road_section in ujson.loads(response)["features"]:
            index_road_id = int(road_section["properties"]["id"].split('_')[0])
            index_road_section_id = int(road_section["properties"]["id"].split('_')[1])

            for element in road_section["geometry"]["coordinates"]:
                all_road_sections.append((element, index_road_id, index_road_section_id))

        # If all_road_sections is empty return None else return all_road_sections
        if len(all_road_sections) > 0:
            return all_road_sections
        else:
            return None

    @staticmethod
    def get_all_road_sections_geodata_in_db():
        all_road_section_geo_data_in_db = []
        all_road_section_geo_data = Scraper.get_geodata_for_all_road_sections()
        road_sections_in_db = []
        count = 0
        for element in Road_section.objects.all():
            road_sections_in_db.append((element.road.Road_number, element.road_section_number))
            count += 1
            print(count)

        for element in all_road_section_geo_data:
            (geo_data, road_id, road_section_id) = element
            if (road_id, road_section_id) in road_sections_in_db:
                all_road_section_geo_data_in_db.append(geo_data)
        return all_road_section_geo_data_in_db

    @staticmethod
    def update_all_road_sections_json():
        print('update_all_road_sections_json has been called')
        all_road_section_geo_data_in_db = Scraper.get_all_road_sections_geodata_in_db()
        with open("traffic_speed_prediction/all_road_sections_geodata.json",
                  "w") as outfile:  # Where should we put the json file?
            json.dump(all_road_section_geo_data_in_db, outfile)
        return all_road_section_geo_data_in_db
