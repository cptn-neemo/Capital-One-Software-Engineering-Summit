import json
from geopy.geocoders import Nominatim

class Battalion:
    def __init__(self, number):
        self.number = number

        #Total number of dispatches in this battalion
        self.total_dispatch_count = 0
        #Total time on dispatch before reaching the destination
        self.total_dispatch_minutes = 0
        #Average time of dispatch
        self.dispatch_time_avg = 0

        # [Medical Incident, Fire, Traffic Collision, Alarms, Other]
        self.dispatch_types = ["Medical Incident", "Fire", "Traffic Collision", "Alarms", "Other"]
        self.dispatch_type_counts = [0,0,0,0,0]
        self.total_dispatch_type_minutes = [0,0,0,0,0]
        self.dispatch_type_time_avgs = [0,0,0,0,0]

        #Most likely dispatch for this Battalion for the time
        self.most_likely_dispatch = []

    #Compute the average dispatch time
    def compute_avg_dispatch(self):
        self.dispatch_time_avg = self.total_dispatch_minutes / self.total_dispatch_count

    #Compute average dispatch times for each type of dispatch
    def compute_type_dispatch_avg(self):
        for i in range(5):
            self.dispatch_type_time_avgs[i] = \
                self.total_dispatch_type_minutes[i] / self.dispatch_type_counts[i]

    #Create a json representation of the Battalion object
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    #Create a string representation of the Battalion object
    def to_string(self):
        retString = "Battalion: " + str(self.number) + '\n' + \
        "Total dispatches: " + str(self.total_dispatch_count) + \
        "\nAverage dispatch time: " + str(round(self.dispatch_time_avg,3)) + '\n'

        for i in range(self.dispatch_types.__len__()):
            retString += self.dispatch_types[i] + '\n   Count: ' + str(round(self.dispatch_type_counts[i],3)) + \
            '\n   Avg dispatch time: ' + str(round(self.dispatch_type_time_avgs[i],3)) + '\n'

        return retString + '\n'