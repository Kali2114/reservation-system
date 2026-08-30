import pytest

import reservation
from user_store import UserStore
from storage import Storage
from reservation_system import ReservationSystem
from . import utils


def test_schema_init_is_idempotent(tmp_path):
    Storage(tmp_path / "test.db")
    Storage(tmp_path / "test.db")


def test_table_exist(tmp_path):
    storage = Storage(tmp_path / "test.db")
    names = {r[0] for r in storage.conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )}
    assert {"users", "reservations"} <= names


def test_save_users_writes_row(tmp_path):
    storage = Storage(tmp_path / "test.db")
    user_store = UserStore()
    user = user_store.register(
        name="test_user", email="test_email", password="test_password"
    )

    storage.save_users(user_store)

    rows = storage.conn.execute("SELECT * FROM users").fetchall()
    assert len(rows) == 1
    row = rows[0]
    assert row["id"] == user.id
    assert row["name"] == user.name
    assert row["email"] == user.email
    assert row["password_hash"] == user.password_hash
    assert row["salt"] == user.salt


def test_save_users_overwrites(tmp_path):
    storage = Storage(tmp_path / "test.db")
    user_store = UserStore()
    user_store.register(
        name="test_user", email="test_email", password="test_password"
    )

    storage.save_users(user_store)
    storage.save_users(user_store)

    count = storage.conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    assert count == 1


def test_round_trip_save_load_users(tmp_path):
    storage = Storage(tmp_path / "test.db")
    user_store = UserStore()
    user1 = user_store.register(
        name="test_user1", email="test_email1", password="test_password1"
    )
    user2 = user_store.register(
        name="test_user2", email="test_email2", password="test_password2"
    )
    storage.save_users(user_store)
    new_storage = Storage(tmp_path / "test.db")
    loaded_users = new_storage.load_users()

    assert len(loaded_users) == 2
    assert loaded_users[user1.email].name == user1.name
    assert loaded_users[user1.email].email == user1.email
    assert loaded_users[user1.email].password_hash == user1.password_hash
    assert loaded_users[user1.email].salt == user1.salt
    assert loaded_users[user2.email].name == user2.name
    assert loaded_users[user2.email].email == user2.email
    assert loaded_users[user2.email].password_hash == user2.password_hash
    assert loaded_users[user2.email].salt == user2.salt


def test_save_reservations(tmp_path):
    storage = Storage(tmp_path / "test.db")
    user_storage = UserStore()
    payload = {
        "name": "test_user",
        "email": "test_email",
        "password": "test_password",
    }
    user = user_storage.register(**payload)
    slot = utils.create_time_slot()
    system = ReservationSystem()
    system.add_reservation(user=user, slot=slot)
    reservation = system.reservations[0]
    storage.save_users(user_storage)
    storage.save_reservations(system)
    rows = storage.conn.execute("SELECT * FROM reservations").fetchall()
    assert len(rows) == 1
    assert rows[0]["user_email"] == user.email
    assert rows[0]["id"] == str(reservation.id)
    assert rows[0]["status"] == "Active"


def test_round_trip_save_load_reservations(tmp_path):
    storage = Storage(tmp_path / "test.db")
    user_storage = UserStore()
    payload = {
        "name": "test_user",
        "email": "test_email",
        "password": "test_password",
    }
    user = user_storage.register(**payload)
    storage.save_users(user_storage)
    system = ReservationSystem()
    system.add_reservation(user=user, slot=utils.create_time_slot())
    reservation = system.reservations[0]
    storage.save_reservations(system)
    result = storage.load_reservations(user_storage)

    assert len(result) == 1
    assert result[0].user.email == user.email
    assert result[0].id == reservation.id
    assert result[0].status == "Active"


def test_unknown_user_load_reservation_raise_value_error(tmp_path):
    storage = Storage(tmp_path / "test.db")
    user_storage = UserStore()
    payload = {
        "name": "test_user",
        "email": "test_email",
        "password": "test_password",
    }
    user = user_storage.register(**payload)
    system = ReservationSystem()
    system.add_reservation(user=user, slot=utils.create_time_slot())
    storage.save_users(user_storage)
    storage.save_reservations(system)
    other_user_store = UserStore()
    with pytest.raises(ValueError):
        storage.load_reservations(other_user_store)




