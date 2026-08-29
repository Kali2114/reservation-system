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


def _restore_user_id_counter(users):
    if users:
        User.id = max(u.id for u in users.values()) + 1


def load_data(path, user_store):
    system = ReservationSystem()
    try:
        with open(path, "r") as f:
            raw_reservations = json.load(f)
    except FileNotFoundError:
        return system

    users = user_store.users
    for raw in raw_reservations:
        user_email = raw["reservation_user"]["user_email"]
        try:
            user = users[user_email]
        except KeyError:
            raise ValueError(f"reservation references unknown user {user_email}")
        system.reservations.append(_reservation_from_dict(raw, user))

    _restore_user_id_counter(users)

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


def _reservation_from_dict(raw, user):
    start_time = datetime.fromisoformat(raw["reservation_slot"]["start_time"])
    end_time = datetime.fromisoformat(raw["reservation_slot"]["end_time"])
    reservation = Reservation(user, TimeSlot(start_time, end_time))
    reservation.id = uuid.UUID(raw["reservation_id"])
    reservation.status = raw["status"]
    return reservation


def save_users(users, path):
    payload = {email: {
        "id": value.id,
        "name": value.name,
        "email": value.email,
        "password_hash": value.password_hash.hex(),
        "salt": value.salt.hex()
    } for email, value in users.items()}
    with open(path, "w") as f:
        json.dump(payload, f)


def load_users(path):
    users = {}
    try:
        with open(path, "r") as f:
            raw_users = json.load(f)
    except FileNotFoundError:
        return users
    for key, value in raw_users.items():
        users[key] = User(
            name=value["name"],
            email=value["email"],
            password_hash=bytes.fromhex(value["password_hash"]),
            salt=bytes.fromhex(value["salt"])
        )
        users[key].id = value["id"]
    _restore_user_id_counter(users)
    return users

