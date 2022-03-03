class Dataobject:
    object_id: int
    roadstation_id: int
    station_name: str
    speed: float
    date: str
    time: str


    def __init__(self, object_id, roadstation_id, station_name, speed, date, time):
        self.object_id = object_id
        self.roadstation_id = roadstation_id
        self.station_name = station_name
        self.speed = speed
        self.date = date
        self.time = time

    def __repr__(self):
        return f"{self.object_id}  RoadstationID:  {self.roadstation_id} station_name: {self.station_name} speed: {self.speed}  date: {self.date}  time: {self.time}"