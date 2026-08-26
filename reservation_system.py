from reservation import Reservation


class ReservationSystem:
    def __init__(self):
        self.reservations = []

    def add_reservation(self, user, slot):
        for reservation in self.reservations:
            if reservation.slot.overlaps_with(slot) and reservation.status == "Active":
                return False
        self.reservations.append(Reservation(user, slot))
        return True

    def cancel_reservation(self, reservation_id):
        for reservation in self.reservations:
            if str(reservation.id) == reservation_id:
                if reservation.status == "Cancelled":
                    return False
                reservation.status = "Cancelled"
                return True
        return False

    def list_reservations(self, user=None):
        if user is None:
            return self.reservations
        return [r for r in self.reservations if r.user.id == user.id]
