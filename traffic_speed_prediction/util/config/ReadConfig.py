import ujson


def read_config():
    with open("../../data.json", "r") as file:
        return ujson.load(file)


def read_secrets():
    with open("../../secrets.json", "r") as file:
        return ujson.load(file)


def convert_to_date(datetime: str):
    time_registered = str(datetime).split("T")
    return time_registered[0], time_registered[1].replace("Z", "")
