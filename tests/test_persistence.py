from user import User
from persistence import load_data, save_data, load_users, save_users
from reservation_system import ReservationSystem
from user_store import UserStore
from datetime import datetime
from . import utils


class TestPersistence:

    def setup_method(self):
        self.system = ReservationSystem()
        self.user_store = UserStore()
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
        path = tmp_path / "users.json"
        self.system.add_reservation(self.user, self.slot)
        self.user.id = 50
        save_data(self.system.reservations, path)
        load_data(path)
        new_user = utils.create_user(name="new_user")
        assert new_user.id == 51

    def test_load_user_id_no_data(self, tmp_path):
        path = tmp_path / "users.json"
        save_data(self.system.reservations, path)
        User.id = 1
        load_data(path)
        new_user = utils.create_user(name="new_user")
        assert new_user.id == 1

    def test_load_cancelled_status(self, tmp_path):
        path = tmp_path / "users.json"
        self.system.add_reservation(self.user, self.slot)
        self.system.reservations[0].status = "Cancelled"
        save_data(self.system.reservations, path)
        result = load_data(path)
        assert result.reservations[0].status == "Cancelled"

    def test_load_users_missing_file(self, tmp_path):
        result = load_users(tmp_path / "missing_file.json")
        assert result == {}

    def test_round_trip_save_load_users(self, tmp_path):
        path = tmp_path / "users.json"
        user = self.user_store.register(
            name="test_user",
            email="test_email",
            password="test_pass",
        )
        save_users(self.user_store.users, path)
        result = load_users(path)
        assert len(result) == 1
        assert result[user.email].email == user.email
        assert result[user.email].id == user.id
        assert result[user.email].name == user.name
        assert result[user.email].password_hash == user.password_hash
        assert result[user.email].salt == user.salt

    def test_login_after_load(self, tmp_path):
        path = tmp_path / "users.json"
        self.user_store.register(name="A", email="a@x.com", password="pw")
        save_users(self.user_store.users, path)
        loaded = UserStore()
        loaded.users = load_users(path)
        assert loaded.login("a@x.com", "pw").email == "a@x.com"

    def test_load_users_restores_id_counter(self, tmp_path):
        path = tmp_path / "users.json"
        user = self.user_store.register(
            name="test_user",
            email="test_email",
            password="test_pass",
        )
        user.id = 500
        save_users(self.user_store.users, path)
        load_users(path)
        assert User.id == 501

