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

    # [Medical Incident, Fire, Traffic Collision, dispatchs, Other]
    @staticmethod
    def get_most_likely_dispatch(dispatch_list, battalion):
        hour_dispatch_type_counts = [[0 for x in range(5)] for y in range(24)]

        for i in range(len(dispatch_list)):
            hour = dispatch_list[i].time
            hour = hour[:2]
            type_of_dispatch = dispatch_list[i].type

            if (type_of_dispatch == 'Medical Incident'):
                hour_dispatch_type_counts[int(hour) - 1][0] += 1
            elif (type_of_dispatch == 'Fire' or type_of_dispatch == 'Structure Fire' or
                  type_of_dispatch == 'Outside Fire' or type_of_dispatch == 'Vehicle Fire'):
                hour_dispatch_type_counts[int(hour) - 1][1] += 1
            elif (type_of_dispatch == 'Traffic Collision'):
                hour_dispatch_type_counts[int(hour)][2] += 1
            elif (type_of_dispatch ==  'dispatchs'):
                hour_dispatch_type_counts[int(hour) - 1][3] += 1
            else:
                hour_dispatch_type_counts[int(hour) - 1][4] += 1

        #Calculate the percent chance of a dispatch at a given time
        for i in range(len(hour_dispatch_type_counts)):
            sum_of_counts = sum(hour_dispatch_type_counts[i])
            cur_hour = hour_dispatch_type_counts[i]
            battalion.most_likely_dispatch.append([round(x / sum_of_counts, 3) for x in cur_hour])

    @staticmethod
    def write_day_counts(day_count_list):
        with open('../sfpd-dispatch/day_counts.txt', 'w') as date_file:
            for date in sorted(day_count_list):
                date_file.write(date + ': ' + str(day_count_list[date]) + '\n')
