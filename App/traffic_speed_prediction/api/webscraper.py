import requests

#Whats this?
from json import *

url = "https://tie.digitraffic.fi/api/beta/weather-history-data/4057"

response = requests.get(url)

js = response.json()

d = js[0]




s = str(d)
s = s.replace("'", "\"")

d["roadStationId"]
d["sensorId"]
d["sensorValue"]
d["measuredTime"]



def tryGet():
    url = "https://tie.digitraffic.fi/api/beta/weather-history-data/4057"
    response = requests.get(url)
    js = response.json()
    d = js[0]
    return js