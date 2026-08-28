import json
from datetime import datetime
import uuid

from reservation import Reservation
from reservation_system import ReservationSystem
from timeslot import TimeSlot
from user import User


def save_data(reservations, path):
    with open(path, "w") as f:
        reservation_list = []
        for reservation in reservations:
            reservation_dict = {
                "reservation_id": str(reservation.id),
                "reservation_user": {
                    "user_id": reservation.user.id,
                    "user_name": reservation.user.name,
                    "user_email": reservation.user.email,
                },
                "reservation_slot": {
                    "start_time": reservation.slot.start_time.isoformat(),
                    "end_time": reservation.slot.end_time.isoformat(),
                },
                "status": reservation.status
            }
            reservation_list.append(reservation_dict)
        json.dump(reservation_list, f)


def load_data(path):
    system = ReservationSystem()
    try:
        with open(path, "r") as f:
            reservations = json.load(f)
            next_user_id = 0
            users = {}
            for reservation in reservations:
                user_id = reservation["reservation_user"]["user_id"]
                if user_id not in users:
                    user = User(reservation["reservation_user"]["user_name"], reservation["reservation_user"]["user_email"])
                    user.id = reservation["reservation_user"]["user_id"]
                    users[user_id] = user
                else:
                    user = users[user_id]
                if user.id >= next_user_id:
                    next_user_id = user.id + 1
                time_slot_start = datetime.fromisoformat(reservation["reservation_slot"]["start_time"])
                time_slot_end = datetime.fromisoformat(reservation["reservation_slot"]["end_time"])
                timeslot = TimeSlot(time_slot_start, time_slot_end)
                read_reservation = Reservation(user, timeslot)
                read_reservation.id = uuid.UUID(reservation["reservation_id"])
                read_reservation.status = reservation["status"]
                system.reservations.append(read_reservation)
            if reservations:
                User.id = next_user_id
        return system
    except FileNotFoundError:
        return system
