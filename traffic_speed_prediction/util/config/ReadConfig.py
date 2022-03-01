def read_config():
    return eval(open("../../data.json").read())


def read_secrets():
    return eval(open("../../secrets.json").read())


def convert_to_date(datetime: str):
    time_registered = str(datetime).split("T")
    return time_registered[0], time_registered[1].replace("Z", "")
