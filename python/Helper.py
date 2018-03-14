from Alarm import Alarm

class Helper:
    @staticmethod
    def compute_difference_time(hour, minute, second):
        # This if statement is used to normalize overnight dispatches. It accounts for if the
        # dispatch time took place over two days
        if hour[1] < hour[0]:
            hour[1] += -(0 - hour[0])
            hour[0] = 0

        total_minute_0 = (hour[0] * 60) + minute[0] + (second[0] / 60)
        total_minute_1 = (hour[1] * 60) + minute[1] + (second[1] / 60)
        return total_minute_1 - total_minute_0

    @staticmethod
    def write_to_txt(path, arr):
        with open(path, 'w') as data_file:
            for i in range(len(arr)):
                data_file.write(arr[i].to_string())
    @staticmethod
    def write_to_json(path, arr, type, num_elements):
        with open(path, 'w') as data_file:
            data_file.write('{\n')
            for i in range(len(arr)):
                data_file.write('"' + type + str(i) + '" : ')
                if i != num_elements - 1:
                    data_file.write(arr[i].toJSON() + ',\n')
                else:
                    data_file.write(arr[i].toJSON() + '\n')
            data_file.write('}')

    @staticmethod
    def get_time(received_time):
        if (type(received_time) is str):
            return received_time[11:19]
        else:
            return "NaN"

    # [Medical Incident, Fire, Traffic Collision, Alarms, Other]
    @staticmethod
    def get_most_likely_dispatch(alarm_list, battalion):
        hour_dispatch_type_counts = [[0 for x in range(5)] for y in range(24)]

        for i in range(len(alarm_list)):
            hour = alarm_list[i].time
            hour = hour[:2]
            type_of_alarm = alarm_list[i].type

            if (type_of_alarm == 'Medical Incident'):
                hour_dispatch_type_counts[int(hour) - 1][0] += 1
            elif (type_of_alarm == 'Fire' or type_of_alarm == 'Structure Fire' or
                  type_of_alarm == 'Outside Fire' or type_of_alarm == 'Vehicle Fire'):
                hour_dispatch_type_counts[int(hour) - 1][1] += 1
            elif (type_of_alarm == 'Traffic Collision'):
                hour_dispatch_type_counts[int(hour)][2] += 1
            elif (type_of_alarm ==  'Alarms'):
                hour_dispatch_type_counts[int(hour) - 1][3] += 1
            else:
                hour_dispatch_type_counts[int(hour) - 1][4] += 1

        #Calculate the percent chance of a dispatch at a given time
        for i in range(len(hour_dispatch_type_counts)):
            sum_of_counts = sum(hour_dispatch_type_counts[i]);
            cur_hour = hour_dispatch_type_counts[i]
            battalion.most_likely_dispatch.append([round(x / sum_of_counts, 3) for x in cur_hour])


            # max_count_index = hour_dispatch_type_counts[i].index(max(hour_dispatch_type_counts[i]))
            # if max_count_index == 0:
            #     battalion.most_likely_dispatch.append('Medical Incident')
            # elif max_count_index == 1:
            #     battalion.most_likely_dispatch.append('Fire')
            # elif max_count_index == 2:
            #     battalion.most_likely_dispatch.append('Traffic Collision')
            # elif max_count_index == 3:
            #     battalion.most_likely_dispatch.append('Alarms')
            # elif max_count_index == 4:
            #     battalion.most_likely_dispatch.append('Other')
            # else:
            #     print('Error: index out of bounds.')
