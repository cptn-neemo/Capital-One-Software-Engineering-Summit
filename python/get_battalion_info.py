import pandas as pd
from Battalion import Battalion
from Helper import Helper
from Dispatch import Dispatch

#Read in the csv into a pandas dataframe
df = pd.read_csv('../sfpd-dispatch/sfpd_dispatch_data_subset.csv')

#Array of battalions to organize statistics
battalions = [Battalion(1), Battalion(2), Battalion(3), Battalion(4), Battalion(5), Battalion(6),
              Battalion(7), Battalion(8), Battalion(9), Battalion(10)]

#List of all 10,000 dispatches from the dataset
dispatch_list = []

#Dictionary containing the amount of dispatches per day
day_count_list = {}

for index, row in df.iterrows():
     #Get the battalion number, B)2 -> 2
     battalion = row['battalion']
     battalion = battalion[2:]

     #Get the received timestamp and the on_scene timestamp
     received_time = row['received_timestamp']
     on_scene_time = row['on_scene_timestamp']

     type_of_call = row['call_type']

     lat = row['latitude']
     long = row['longitude']

     #Get the day from received time, in format yyyy-dd-mm
     day = received_time[:10]

     #Check to see if the day is currently in dictionary
     if day in day_count_list:
          #If it is, increase the count
         day_count_list[day] = day_count_list.get(day) + 1
     else:
         #Else insert it with a count of 1
         day_count_list[day] = 1

     #If either timestamp is NaN, it will be considered a float
     if (type(received_time) is str and type(on_scene_time) is str):
          #Parse in the hours, minutes, and seconds
          hour = [int(received_time[11:13]), int(on_scene_time[11:13])]
          minute = [int(received_time[14:16]), int(on_scene_time[14:16])]
          second = [int(received_time[17:19]), int(on_scene_time[17:19])]

          #Get the minute difference: on_scene - call_received
          minute_difference = Helper.compute_difference_time(hour, minute, second)

          #Check for extreme outliers that will affect the average
          if (minute_difference < 60):
               #Increase the total counts and dispatch minutes
               battalions[int(battalion) - 1].total_dispatch_count += 1
               battalions[int(battalion) - 1].total_dispatch_minutes += minute_difference

               #Get the specific type of call data
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

          #For the dispatch list get the full timestamp. Then append a new dispatch to the list
          dispatch_received_time = Helper.get_time(received_time)
          dispatch_list.append(Dispatch(type_of_call, dispatch_received_time, battalion, lat, long, index))


#Compute various statistics for the battalions
for i in range(len(battalions)):
     battalions[i].compute_avg_dispatch()
     battalions[i].compute_type_dispatch_avg()
     Helper.get_most_likely_dispatch(dispatch_list, battalions[i])

#Write the data to their respective files
Helper.write_to_txt('../sfpd-dispatch/battalion-data.txt', battalions)
Helper.write_to_json('../sfpd-dispatch/batallion-data.json', battalions, 'Battalion')
Helper.write_to_json('../sfpd-dispatch/dispatch.json', dispatch_list, 'Dispatch')
Helper.write_day_counts(day_count_list)