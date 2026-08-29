# reservation-system

A command-line reservation system in Python. Users register and log in, then
book time slots; overlapping bookings for an active reservation are rejected.
Accounts and reservations are persisted to JSON between runs.

## Requirements

- Python 3.12+
- No runtime dependencies (standard library only)
- `pytest` to run the tests

## Running

```bash
python main.py
```

On start you get the auth menu:

```
1. to Register | 2. to Login | 3. to Exit
```

After logging in, the reservation menu:

```
1. Add Reservation
2. Cancel Reservation
3. List Reservations
4. Logout
```

- **Add** — enter a start and end time as `YYYY-MM-DD HH:MM`. The booking is
  rejected if it overlaps an existing active reservation.
- **Cancel** — enter the reservation id shown by *List*.
- **List** — shows your own reservations.

State is written to `data.json` (reservations) and `users.json` (accounts) on
exit and reloaded on the next run. Both files are gitignored; passwords are
stored as a PBKDF2-SHA256 hash with a per-user salt, never in plain text.

## Tests

```bash
pytest
```

## Layout

| Module | Responsibility |
| --- | --- |
| `main.py` | CLI: auth menu, reservation menu, wiring persistence |
| `timeslot.py` | `TimeSlot` — validates a start/end pair, overlap check |
| `reservation.py` | `Reservation` — a user + slot + status |
| `reservation_system.py` | `ReservationSystem` — add / cancel / list, conflict rules |
| `user.py` | `User` — name, email, password hash, salt |
| `security.py` | `hash_password` / `verify_password` (PBKDF2-SHA256) |
| `user_store.py` | `UserStore` — register / login, keyed by email |
| `persistence.py` | Load and save reservations and users as JSON |
| `storage.py` | SQLite-backed storage (in progress, not yet wired in) |
