import json

class Dispatch:
    def __init__(self, type, time, battalion_number, lat, long, id):
        #Type of the dispatch
        self.type = type

        #Time the dispatch occured
        self.time = time

        #Battalion the dispatch was in
        self.battalion_number = battalion_number

        #Latitude and longitudes of the dispatch
        self.lat = lat
        self.long = long

        #Dispatch ID
        self.id = id

    #Create a csv_string of the current dispatch
    def to_csv_string(self):
        return str(self.id) + ',' + str(self.time) + ',' + str(self.battalion_number) + ',' \
        + str(self.lat) + ',' + str(self.long) + ',' + self.id

    #Create a json representation of the dispatch object
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)