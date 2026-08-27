from reservation_system import ReservationSystem
from . import utils


class TestReservationSystem:

    def setup_method(self):
        self.system = ReservationSystem()
        self.user = utils.create_user()
        self.slot = utils.create_time_slot()
        self.reservation = utils.create_reservation(user=self.user, slot=self.slot)


    def test_add_reservation(self):
        self.system.add_reservation(self.user, self.slot)
        assert self.system.reservations[0].user == self.user
        assert self.system.reservations[0].slot == self.slot
        assert len(self.system.reservations) == 1