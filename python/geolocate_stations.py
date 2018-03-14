from geopy.geocoders import Nominatim
import json

#Declare the geolocator, and the dictionary used to store the station locations
geolocator = Nominatim()
stations = {}

address_file = open('station_addresses.txt', 'r').read()

#Keep track of the station number to use as key
station_number = 1
for line in address_file.splitlines():
    #While loop is used because the geolocator does not work everytime for some reason. Loop is used to keep requesting
    #The station until a valid location is received
    while(True):
        try:
            location = geolocator.geocode(line + " SF")
            stations[station_number] = [location.latitude, location.longitude]
            station_number += 1
            break
        except:
            #Used to check if repeat addresses cannot be obtained.
            print(line)

#Dump the stations dict into a json file
with open('../sfpd-dispatch/station_addresses.json', 'w') as out_file:
    json.dump(stations, out_file)