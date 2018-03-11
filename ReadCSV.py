import numpy as np
import pandas as pd
from Battalion import Battalion


def compute_difference_time(hour, minute, second):

     #This if statement is used to normalize overnight dispatches. It accounts for if the
     #dispatch time took place over two days
     if hour[1] < hour[0]:
          hour[1] += -(0 - hour[0])
          hour[0] = 0

     total_minute_0 = (hour[0] * 60) + minute[0] + (second[0] / 60)
     total_minute_1 = (hour[1] * 60) + minute[1] + (second[1] / 60)
     return total_minute_1 - total_minute_0


df = pd.read_csv('./sfpd-dispatch/sfpd_dispatch_data_subset.csv')

battalionCount = [0,0,0,0,0,0,0,0,0]
battalion_dispatch_count = [0,0,0,0,0,0,0,0,0]
battalion_dispatch_total_dif = [0,0,0,0,0,0,0,0,0]

battalions = [Battalion(1), Battalion(2), Battalion(3), Battalion(4), Battalion(5), Battalion(6),
              Battalion(7), Battalion(8), Battalion(9)]

#[Medical Incident, Fire, Traffic Collision, Alarms, Other]
type_of_call_count = [0,0,0,0,0]
type_of_call_total = [0,0,0,0,0]


for index, row in df.iterrows():
     battalion = row['battalion']
     battalion = battalion[2:]
     battalionCount[int(battalion) - 1] += 1

     received_time = row['received_timestamp']
     on_scene_time = row['on_scene_timestamp']

     type_of_call = row['call_type']

     #2018-01-13 13:17:25.000000 UTC

     #If either timestamp is NaN, it will be considered a float
     if (type(received_time) is str and type(on_scene_time) is str):
          hour = [int(received_time[11:13]), int(on_scene_time[11:13])]
          minute = [int(received_time[14:16]), int(on_scene_time[14:16])]
          second = [int(received_time[17:19]), int(on_scene_time[17:19])]
          minute_difference = compute_difference_time(hour, minute, second)

          if (minute_difference < 120):
               battalions[int(battalion) - 1].total_dispatch_count += 1
               battalions[int(battalion) - 1].total_dispatch_minutes += minute_difference

          if (type_of_call == "Medical Incident"):
               battalions[int(battalion) - 1].dispatch_type_counts[0] += 1
               battalions[int(battalion) - 1].total_dispatch_type_minutes[0] += minute_difference
          elif ("Fire" in type_of_call):
               battalions[int(battalion) - 1].dispatch_type_counts[1] += 1
               battalions[int(battalion) - 1].total_dispatch_type_minutes[1] += minute_difference
          elif (type_of_call == "Traffic Collision"):
               battalions[int(battalion) - 1].dispatch_type_counts[2] += 1
               battalions[int(battalion) - 1].total_dispatch_type_minutes[2] += minute_difference
          elif (type_of_call == "Alarms"):
               battalions[int(battalion) - 1].dispatch_type_counts[3] += 1
               battalions[int(battalion) - 1].total_dispatch_type_minutes[3] += minute_difference
          else:
               battalions[int(battalion) - 1].dispatch_type_counts[4] += 1
               battalions[int(battalion) - 1].total_dispatch_type_minutes[4] += minute_difference




print(battalionCount)
print("Battalion 1: " + str(battalions[1].dispatch_type_counts[1]) )






