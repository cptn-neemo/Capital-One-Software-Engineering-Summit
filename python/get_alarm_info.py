import pandas as pd
from Alarm import Alarm

df = pd.read_csv('../sfpd-dispatch/sfpd_dispatch_data_subset.csv')
alarm_list = []

def getTime(received_time):
    if (type(received_time) is str):
        return received_time[11:19]
    else:
        return "NaN"



for index, row in df.iterrows():
    lat = row['latitude']
    long = row['longitude']
    type_of_call = row['call_type']
    time = getTime(row['received_timestamp'])
    id = index

    alarm_list.append(Alarm(type_of_call,time, lat, long, id))

with open('../sfpd-dispatch/alarms.json', 'w') as data_file:
    data_file.write('{\n')
    for i in range(len(alarm_list)):
        data_file.write('"Alarm ' + str(alarm_list[i].id) + '" : ')
        if i != alarm_list.__len__() - 1:
            data_file.write(alarm_list[i].toJSON() + ',\n')
        else:
            data_file.write(alarm_list[i].toJSON() + '\n')
    data_file.write('}')



