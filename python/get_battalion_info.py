import pandas as pd
from Battalion import Battalion
from Helper import Helper
from Alarm import Alarm

df = pd.read_csv('../sfpd-dispatch/sfpd_dispatch_data_subset.csv')


battalions = [Battalion(1), Battalion(2), Battalion(3), Battalion(4), Battalion(5), Battalion(6),
              Battalion(7), Battalion(8), Battalion(9), Battalion(10)]

alarm_list = []

for index, row in df.iterrows():
     battalion = row['battalion']
     battalion = battalion[2:]

     received_time = row['received_timestamp']
     on_scene_time = row['on_scene_timestamp']

     type_of_call = row['call_type']



     lat = row['latitude']
     long = row['longitude']

     #If either timestamp is NaN, it will be considered a float
     if (type(received_time) is str and type(on_scene_time) is str):
          hour = [int(received_time[11:13]), int(on_scene_time[11:13])]
          minute = [int(received_time[14:16]), int(on_scene_time[14:16])]
          second = [int(received_time[17:19]), int(on_scene_time[17:19])]
          minute_difference = Helper.compute_difference_time(hour, minute, second)

          #Check for extreme outliers that will affect the average
          if (minute_difference < 60):
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

          alarm_received_time = Helper.get_time(received_time)
          alarm_list.append(Alarm(type_of_call, alarm_received_time, battalion, lat, long, index))


for i in range(len(battalions)):
     battalions[i].compute_avg_dispatch()
     battalions[i].compute_type_dispatch_avg()
     Helper.get_most_likely_dispatch(alarm_list, battalions[i])


Helper.write_to_txt('../sfpd-dispatch/battalion-data.txt', battalions)
Helper.write_to_json('../sfpd-dispatch/batallion-data.json', battalions, 'Battalion', len(battalions))










