from user import User
from persistence import load_data, save_data
from reservation_system import ReservationSystem
from datetime import datetime
from . import utils


class TestPersistence:

    def setup_method(self):
        self.system = ReservationSystem()
        self.user = utils.create_user()
        self.slot = utils.create_time_slot()
        self.other_slot = utils.create_time_slot(
            start_time=datetime(2020, 11, 1, 0, 0, 0),
            end_time=datetime(2020, 11, 2, 0, 0, 0),
        )

    def test_load_data_missing_file(self, tmp_path):
        result = load_data(tmp_path / "missing_file.json")
        assert result.reservations == []

    def test_round_trip_save_load(self, tmp_path):
        path = tmp_path / "data.json"
        self.system.add_reservation(self.user, self.slot)

        save_data(self.system.reservations, path)
        result = load_data(path)

        assert len(result.reservations) == 1
        r = result.reservations[0]
        assert r.user.name == self.user.name
        assert r.user.email == self.user.email
        assert r.user.id == self.user.id
        assert r.slot.start_time == self.slot.start_time
        assert r.slot.end_time == self.slot.end_time
        assert r.status == "Active"
        assert r.id == self.system.reservations[0].id

    def test_dedup_save_data(self, tmp_path):
        path = tmp_path / "data.json"
        self.system.add_reservation(self.user, self.slot)
        self.system.add_reservation(self.user, self.other_slot)
        save_data(self.system.reservations, path)
        result = load_data(path)
        assert len(result.reservations) == 2
        assert result.reservations[0].user is result.reservations[1].user

    def test_load_user_id(self, tmp_path):
        path = tmp_path / "data.json"
        self.system.add_reservation(self.user, self.slot)
        self.user.id = 50
        save_data(self.system.reservations, path)
        load_data(path)
        new_user = utils.create_user(name="new_user")
        assert new_user.id == 51

    def test_load_user_id_no_data(self, tmp_path):
        path = tmp_path / "data.json"
        save_data(self.system.reservations, path)
        User.id = 1
        load_data(path)
        new_user = utils.create_user(name="new_user")
        assert new_user.id == 1

    def test_load_cancelled_status(self, tmp_path):
        path = tmp_path / "data.json"
        self.system.add_reservation(self.user, self.slot)
        self.system.reservations[0].status = "Cancelled"
        save_data(self.system.reservations, path)
        result = load_data(path)
        assert result.reservations[0].status == "Cancelled"