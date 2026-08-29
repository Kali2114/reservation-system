from datetime import datetime
from persistence import load_data, save_data
from timeslot import TimeSlot
from user_store import UserStore


def run(system, user_store):
    print("Welcome to the Reservation System")
    while True:
        try:
            first = int(input("1. to Register | 2. to Login | 3. to Exit"))
        except ValueError:
            print("Please choose an option")
            continue
        if first == 1:
            login = input("Name: ")
            email = input("Email: ")
            password = input("Password: ")
            try:
                user_store.register(login, email, password)
            except ValueError as e:
                print(e)
                continue
            print("Registered")
            continue
        elif first == 2:
            email = input("Email: ")
            password = input("Password: ")
            try:
                current_user = user_store.login(email, password)
            except ValueError as e:
                print(e)
                continue
        elif first == 3:
            print("Bye")
            return
        else:
            print("Please choose an option")
            continue
        while True:
            print("1. Add Reservation")
            print("2. Cancel Reservation")
            print("3. List Reservations")
            print("4. Logout")
            try:
                choice = int(input("Choose an option: "))
            except ValueError:
                print("Please choose an option")
                continue
            if choice == 1:
                start_time = input("Enter start time YYYY-MM-DD HH:MM: ")
                end_time = input("Enter end time YYYY-MM-DD HH:MM: ")
                try:
                    timeslot = TimeSlot(datetime.strptime(start_time, "%Y-%m-%d %H:%M"), datetime.strptime(end_time, "%Y-%m-%d %H:%M"))
                except ValueError:
                    print("Please enter a valid timeslot")
                    continue
                if system.add_reservation(current_user, timeslot):
                    print("Reservation added")
                else:
                    print("Reservation not added")
            elif choice == 2:
                reservation_id = input("Enter reservation ID: ")
                if system.cancel_reservation(reservation_id):
                    print("Reservation canceled")
                else:
                    print("Reservation not found or already cancelled")
            elif choice == 3:
                for r in system.list_reservations(current_user.id):
                    print(f"{r.id} | {r.user.name} | {r.slot.start_time} - {r.slot.end_time} | {r.status}")
            elif choice == 4:
                break


def main():
    system = load_data("data.json")
    user_store = UserStore()
    print("System loaded")
    run(system, user_store)
    save_data(system.reservations, "data.json")


if __name__ == '__main__':
    main()
