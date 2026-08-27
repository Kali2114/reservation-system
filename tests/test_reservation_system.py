from reservation_system import ReservationSystem
from . import utils
from datetime import datetime


class TestReservationSystem:

    def setup_method(self):
        self.system = ReservationSystem()
        self.user = utils.create_user()
        self.slot = utils.create_time_slot()
        self.reservation = utils.create_reservation(user=self.user, slot=self.slot)

    def test_add_reservation(self):
        assert self.system.add_reservation(self.user, self.slot) is True
        assert self.system.reservations[0].user == self.user
        assert self.system.reservations[0].slot == self.slot
        assert len(self.system.reservations) == 1

    def test_add_reservation_rejects_overlapping_slot(self):
        self.system.add_reservation(self.user, self.slot)
        assert self.system.add_reservation(self.user, self.slot) is False
        assert len(self.system.reservations) == 1

    def test_add_reservation_accept_overlap_cancelled(self):
        self.system.add_reservation(self.user, self.slot)
        self.system.reservations[0].status = "Cancelled"
        assert self.system.add_reservation(self.user, self.slot) is True
        assert len(self.system.reservations) == 2

    def test_add_second_reservation_successful(self):
        self.system.add_reservation(self.user, self.slot)
        new_slot = utils.create_time_slot(start_time= datetime(2020, 11, 1, 0   , 0, 0), end_time=datetime(2020, 11, 2, 0, 0, 0),)
        assert self.system.add_reservation(self.user, new_slot) is True
        assert len(self.system.reservations) == 2

    def test_cancel_reservation_successful(self):
        self.system.add_reservation(self.user, self.slot)
        reservation_id = self.system.reservations[0].id
        assert self.system.cancel_reservation(str(reservation_id)) is True
        assert self.system.reservations[0].status == "Cancelled"

    def test_cancel_reservation_already_cancelled(self):
        self.system.add_reservation(self.user, self.slot)
        self.system.reservations[0].status = "Cancelled"
        reservation_id = self.system.reservations[0].id
        assert self.system.cancel_reservation(str(reservation_id)) is False

    def test_cancel_reservation_no_exist(self):
        self.system.add_reservation(self.user, self.slot)
        assert self.system.cancel_reservation("4") is False


