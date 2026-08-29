import json
from datetime import datetime
import uuid

from reservation import Reservation
from reservation_system import ReservationSystem
from timeslot import TimeSlot
from user import User


def save_data(reservations, path):
    payload = [_reservation_to_dict(r) for r in reservations]
    with open(path, "w") as f:
        json.dump(payload, f)


def load_data(path):
    system = ReservationSystem()
    try:
        with open(path, "r") as f:
            raw_reservations = json.load(f)
    except FileNotFoundError:
        return system

    users = {}
    for raw in raw_reservations:
        user = _get_or_create_user(raw["reservation_user"], users)
        system.reservations.append(_reservation_from_dict(raw, user))

    if users:
        User.id = max(user.id for user in users.values()) + 1

    return system


def _reservation_to_dict(reservation):
    return {
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
        "status": reservation.status,
    }


def _get_or_create_user(raw_user, users):
    user_id = raw_user["user_id"]
    if user_id not in users:
        user = User(raw_user["user_name"], raw_user["user_email"])
        user.id = user_id
        users[user_id] = user
    return users[user_id]


def _reservation_from_dict(raw, user):
    start_time = datetime.fromisoformat(raw["reservation_slot"]["start_time"])
    end_time = datetime.fromisoformat(raw["reservation_slot"]["end_time"])
    reservation = Reservation(user, TimeSlot(start_time, end_time))
    reservation.id = uuid.UUID(raw["reservation_id"])
    reservation.status = raw["status"]
    return reservation
