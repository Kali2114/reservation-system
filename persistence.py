import json


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