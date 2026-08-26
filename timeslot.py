from datetime import datetime


class TimeSlot:
    def __init__(self, start_time, end_time):
        if not isinstance(start_time, datetime) or not isinstance(end_time, datetime):
            raise TypeError("start_time and end_time must be of type datetime")
        if start_time >= end_time:
            raise ValueError("start_time must be before end_time")
        self.start_time = start_time
        self.end_time = end_time

    def overlaps_with(self, other):
        if self.end_time <= other.start_time or other.end_time <= self.start_time:
            return False
        return True