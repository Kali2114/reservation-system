from user_store import UserStore
from storage import Storage


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


