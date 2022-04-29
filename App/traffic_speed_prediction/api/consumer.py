import imp
import json
from pprint import pprint
import string
import requests
from urllib.request import urlopen

#Do we actually use this?



def get_weather_station_data(id) :
    url = "https://tie.digitraffic.fi/api/v1/data/weather-data/" + str(id)

    r = requests.get(url)

    data = json.loads(r.text)

    for item in data['weatherStations'][0]['sensorValues']:
        sid = item['id']
        sname = item['name']


get_weather_station_data(2023)