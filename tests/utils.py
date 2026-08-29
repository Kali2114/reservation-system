from reservation import Reservation
from user import User
from datetime import datetime
from timeslot import TimeSlot


def create_user(**kwargs):
    data = {
        "name": "test_user",
        "email": "test_email",
        "password": "test_password",
        "salt": "test_salt",
    }
    data.update(kwargs)
    return User(**data)


def create_time_slot(**kwargs):
    data = {
        "start_time": datetime(2020, 10, 1, 0, 0, 0),
        "end_time": datetime(2020, 10, 2, 0, 0, 0),
    }
    data.update(kwargs)
    return TimeSlot(**data)


def create_reservation(**kwargs):
    data = {
        "user": create_user(),
        "slot": create_time_slot(),
    }
    data.update(kwargs)
    return Reservation(**data)
