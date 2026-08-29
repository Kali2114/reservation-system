from storage import Storage


def test_schema_init_is_idempotent(tmp_path):
    Storage(tmp_path / "test.db")
    Storage(tmp_path / "test.db")\


def test_table_exist(tmp_path):
    storage = Storage(tmp_path / "test.db")
    names = {r[0] for r in storage.conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )}
    assert {"users", "reservations"} <= names