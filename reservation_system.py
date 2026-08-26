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