import main
from reservation_system import ReservationSystem
from user_store import UserStore


def fake_input(answers):
    """Turn a list of answers into a drop-in replacement for input().

    Each call to input() returns the next item. input() is always called
    with the prompt string, so the replacement must accept one argument.
    """
    it = iter(answers)
    return lambda prompt="": next(it)


# Register a user and log in as them, leaving the session at the
# reservation menu.
LOGIN_PREFIX = [
    "1", "Alice", "alice@example.com", "secret",   # 1. Register
    "2", "alice@example.com", "secret",            # 2. Login
]

# Leave the reservation menu (4. Logout), then the auth menu (3. Exit).
LOGOUT_EXIT = ["4", "3"]


class TestMain:

    def setup_method(self):
        self.system = ReservationSystem()
        self.user_store = UserStore()

    def drive(self, answers, monkeypatch, capsys):
        monkeypatch.setattr("builtins.input", fake_input(answers))
        main.run(self.system, self.user_store)
        return capsys.readouterr().out

    # --- auth menu ----------------------------------------------------------

    def test_exit_from_auth_menu(self, monkeypatch, capsys):
        out = self.drive(["3"], monkeypatch, capsys)
        assert "Bye" in out

    def test_invalid_auth_choice(self, monkeypatch, capsys):
        out = self.drive(["abc", "3"], monkeypatch, capsys)
        assert "Please choose an option" in out

    def test_register_then_login(self, monkeypatch, capsys):
        out = self.drive([*LOGIN_PREFIX, *LOGOUT_EXIT], monkeypatch, capsys)
        assert "Registered" in out
        assert "alice@example.com" in self.user_store.users

    def test_register_duplicate_email(self, monkeypatch, capsys):
        answers = [
            "1", "Alice", "alice@example.com", "secret",
            "1", "Bob", "alice@example.com", "other",
            "3",
        ]
        out = self.drive(answers, monkeypatch, capsys)
        assert "email already registered" in out

    def test_login_wrong_password(self, monkeypatch, capsys):
        answers = [
            "1", "Alice", "alice@example.com", "secret",
            "2", "alice@example.com", "wrong",
            "3",
        ]
        out = self.drive(answers, monkeypatch, capsys)
        assert "invalid email or password" in out

    # --- reservation menu -------------------------------------------------------

    def test_add_reservation_happy_path(self, monkeypatch, capsys):
        answers = [
            *LOGIN_PREFIX,
            "1", "2020-10-01 00:00", "2020-10-02 00:00",
            *LOGOUT_EXIT,
        ]
        out = self.drive(answers, monkeypatch, capsys)
        assert "Reservation added" in out
        assert len(self.system.reservations) == 1
        assert self.system.reservations[0].user.email == "alice@example.com"

    def test_add_reservation_overlapping(self, monkeypatch, capsys):
        answers = [
            *LOGIN_PREFIX,
            "1", "2020-10-01 00:00", "2020-10-02 00:00",
            "1", "2020-10-01 12:00", "2020-10-02 06:00",
            *LOGOUT_EXIT,
        ]
        out = self.drive(answers, monkeypatch, capsys)
        assert "Reservation not added" in out
        assert len(self.system.reservations) == 1

    def test_add_reservation_invalid_timeslot(self, monkeypatch, capsys):
        answers = [
            *LOGIN_PREFIX,
            "1", "banana", "2020-10-01 00:00",
            *LOGOUT_EXIT,
        ]
        out = self.drive(answers, monkeypatch, capsys)
        assert "Please enter a valid timeslot" in out
        assert len(self.system.reservations) == 0

    def test_invalid_menu_choice(self, monkeypatch, capsys):
        answers = [*LOGIN_PREFIX, "abc", *LOGOUT_EXIT]
        out = self.drive(answers, monkeypatch, capsys)
        assert "Please choose an option" in out

    def test_cancel_unknown_id(self, monkeypatch, capsys):
        answers = [*LOGIN_PREFIX, "2", "nonexistent-id", *LOGOUT_EXIT]
        out = self.drive(answers, monkeypatch, capsys)
        assert "Reservation not found or already cancelled" in out

    def test_list_shows_own_reservations(self, monkeypatch, capsys):
        answers = [
            *LOGIN_PREFIX,
            "1", "2020-10-01 00:00", "2020-10-02 00:00",
            "3",
            *LOGOUT_EXIT,
        ]
        out = self.drive(answers, monkeypatch, capsys)
        assert "Reservation added" in out
        assert "Alice" in out


class TestMainPersistence:
    """main() drives a full load -> run -> save cycle against a real db file."""

    def test_account_survives_restart(self, tmp_path, monkeypatch, capsys):
        db = tmp_path / "reservate.db"

        # run 1: register, then exit
        monkeypatch.setattr(
            "builtins.input", fake_input(["1", "Alice", "a@x.com", "pw", "3"])
        )
        main.main(db_path=db)
        capsys.readouterr()

        # run 2: the account is still there, so login reaches the menu
        monkeypatch.setattr(
            "builtins.input", fake_input(["2", "a@x.com", "pw", "4", "3"])
        )
        main.main(db_path=db)
        out = capsys.readouterr().out
        assert "invalid email or password" not in out
        assert "Add Reservation" in out

    def test_reservation_survives_restart(self, tmp_path, monkeypatch, capsys):
        db = tmp_path / "reservate.db"

        monkeypatch.setattr("builtins.input", fake_input([
            "1", "Alice", "a@x.com", "pw",
            "2", "a@x.com", "pw",
            "1", "2020-10-01 00:00", "2020-10-02 00:00",
            "4", "3",
        ]))
        main.main(db_path=db)
        capsys.readouterr()

        monkeypatch.setattr(
            "builtins.input", fake_input(["2", "a@x.com", "pw", "3", "4", "3"])
        )
        main.main(db_path=db)
        out = capsys.readouterr().out
        assert "2020-10-01 00:00:00" in out
        assert "Alice" in out

    def test_fresh_db_starts_empty(self, tmp_path, monkeypatch, capsys):
        db = tmp_path / "reservate.db"
        monkeypatch.setattr("builtins.input", fake_input(["3"]))
        main.main(db_path=db)
        out = capsys.readouterr().out
        assert "System loaded" in out
        assert "Bye" in out
