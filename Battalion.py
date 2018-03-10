class Battalion:
    def __init__(self, number):
        self.battalion_number = number
        self.total_dispatch_count = 0
        self.total_dispatch_minutes = 0
        self.dispatch_time_avg = 0
        self.dispatch_type_counts = [0,0,0,0,0]
        self.total_dispatch_type_minutes = [0,0,0,0,0]
        self.dispatch_type_time_avgs = [0,0,0,0,0]

    def compute_avg_dispatch(self):
        self.dispatch_time_avg = self.total_dispatch_minutes / self.total_dispatch_count

    def compute_type_dispatch_avg(self):
        for i in range(5):
            self.dispatch_type_time_avgs[i] = \
                self.total_dispatch_type_minutes[i] / self.dispatch_type_counts[i]