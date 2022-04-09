import ujson


class Config:

    @staticmethod
    def read_config():
        with open("data.json", "r") as file:
            return ujson.load(file)

    @staticmethod
    def read_secrets():
        with open("../../secrets.json", "r") as file:
            return ujson.load(file)

    @staticmethod
    def convert_to_date(datetime: str):
        time_registered = datetime.split("T")
        return time_registered[0], time_registered[1].replace("Z", "")
