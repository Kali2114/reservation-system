import sqlite3
import uuid
from datetime import datetime

from user import User
from reservation import Reservation
from reservation_system import ReservationSystem
from timeslot import TimeSlot
from user_store import UserStore


class Storage:
    def __init__(self, path):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.conn.execute("""PRAGMA foreign_keys=ON""")
        self.conn.row_factory = sqlite3.Row
        self.init_schema()

    def init_schema(self):
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL,
            salt BLOB NOT NULL
            )"""
        )

        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS reservations (
            id TEXT PRIMARY KEY,
            user_email TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE
            )"""
        )
        self.conn.commit()

    def save_users(self, user_store):
        with self.conn:
            self.conn.execute("DELETE FROM users")
            for user in user_store.users.values():
                cur = self.conn.execute(
                    """INSERT INTO users (name, email, password_hash, salt) VALUES (?, ?, ?, ?)
                    """,
                    (
                        user.name,
                        user.email,
                        user.password_hash,
                        user.salt,
                    )
                )
                user.id = cur.lastrowid

    def load_users(self):
        users = {}
        for row in self.conn.execute(
            "SELECT id, name, email, password_hash, salt FROM users"
        ):
            user = User(row["name"], row["email"], row["password_hash"], row["salt"])
            user.id = row["id"]
            users[row["email"]] = user
        return users

    def save_reservations(self, system):
        with self.conn:
            self.conn.execute("DELETE FROM reservations")
            for reservation in system.reservations:
                self.conn.execute(
                    """INSERT INTO reservations (id, user_email, start_time, end_time, status) VALUES (?, ?, ?, ?, ?)""",(
                    str(reservation.id),
                    reservation.user.email,
                    reservation.slot.start_time.isoformat(),
                    reservation.slot.end_time.isoformat(),
                    reservation.status
                    )
                )

    def load_reservations(self, user_storage):
        reservations = []
        for row in self.conn.execute(
            "SELECT id, user_email, start_time, end_time, status FROM reservations"
        ):
            try:
                user = user_storage.users[row["user_email"]]
            except KeyError:
                raise ValueError(f"reservation references unknown user {row['user_email']}")
            start_time = datetime.fromisoformat(row["start_time"])
            end_time = datetime.fromisoformat(row["end_time"])
            slot = TimeSlot(start_time, end_time)
            reservation = Reservation(
                user,
                slot,
            )
            reservation.id = uuid.UUID(row["id"])
            reservation.status = row["status"]
            reservations.append(reservation)
        return reservations

    def load(self):
        user_store = UserStore()
        user_store.users = self.load_users()
        system = ReservationSystem()
        system.reservations = self.load_reservations(user_store)
        return system, user_store

    def save(self, system, user_store):
        self.save_users(user_store)
        self.save_reservations(system)

    def close(self):
        self.conn.close()

