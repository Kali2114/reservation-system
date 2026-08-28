import main
from reservation_system import ReservationSystem


def fake_input(answers):
    """Turn a list of answers into a drop-in replacement for input().

    Each call to input() returns the next item. input() is always called
    with the prompt string, so the replacement must accept one argument.
    """
    it = iter(answers)
    return lambda prompt="": next(it)


class TestMain:

    def setup_method(self):
        self.system = ReservationSystem()

    def test_add_reservation_happy_path(self, monkeypatch, capsys):
        answers = [
            "1",
            "Alice",
            "alice@example.com",
            "2020-10-01 00:00",
            "2020-10-02 00:00",
            "4",
        ]
        monkeypatch.setattr("builtins.input", fake_input(answers))

        main.run(self.system)

        out = capsys.readouterr().out
        assert "Reservation added" in out
        assert len(self.system.reservations) == 1

    def test_add_reservation_overlapping_path(self, monkeypatch, capsys):
        answers = [
            "1",
            "Alice",
            "alice@example.com",
            "2020-10-01 00:00",
            "2020-10-02 00:00",

            "1",
            "Alice",
            "alice@example.com",
            "2020-10-01 23:59",
            "2020-10-02 10:00",
            "4",
        ]
        monkeypatch.setattr("builtins.input", fake_input(answers) )
        main.run(self.system)
        out = capsys.readouterr().out
        assert "Reservation not added" in out
        assert len(self.system.reservations) == 1

    def test_invalid_menu_choice(self, monkeypatch, capsys):
        answers = [
            "abs",
            "4",
        ]

        monkeypatch.setattr("builtins.input", fake_input(answers))
        main.run(self.system)
        out = capsys.readouterr().out
        assert "Please choose an option" in out

    def test_cancel_unkown_id(self, monkeypatch, capsys):
        answers = [
            "2",
            "nope",
            "4"
        ]

        monkeypatch.setattr("builtins.input", fake_input(answers))
        main.run(self.system)
        out = capsys.readouterr().out
        assert "Reservation not found or already cancelled" in out

    def test_list_bad_user_id(self, monkeypatch, capsys):
        answers = [
            "3",
            "abc",
            "4"
        ]
        monkeypatch.setattr("builtins.input", fake_input(answers))
        main.run(self.system)
        out = capsys.readouterr().out
        assert "Please choose an ID" in out
