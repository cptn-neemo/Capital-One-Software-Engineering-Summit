import json

class Alarm:
    def __init__(self, type, time, battalion_number, lat, long, id):
        self.type = type
        self.time = time
        self.battalion_number = battalion_number
        self.lat = lat
        self.long = long
        self.id = id

    def to_csv_string(self):
        return str(self.id) + ',' + str(self.time) + ',' + str(self.battalion_number) + ',' \
        + str(self.lat) + ',' + str(self.long) + ',' + self.id

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)