from reservation_system import ReservationSystem
from reservation import Reservation
from datetime import datetime
from persistence import load_data, save_data
from timeslot import TimeSlot
from user import User


def run(system):
    print("Welcome to the Reservation System")
    while True:
        print("1. Add Reservation")
        print("2. Cancel Reservation")
        print("3. List Reservations")
        print("4. Exit")
        try:
            choice = int(input("Choose an option: "))
        except ValueError:
            print("Please choose an option")
            continue
        if choice == 1:
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            user = User(name=name, email=email)
            start_time = input("Enter start time YYYY-MM-DD HH:MM: ")
            end_time = input("Enter end time YYYY-MM-DD HH:MM: ")
            timeslot = TimeSlot(datetime.strptime(start_time, "%Y-%m-%d %H:%M"), datetime.strptime(end_time, "%Y-%m-%d %H:%M"))
            if system.add_reservation(user, timeslot):
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
            try:
                user_id = int(input("Enter user ID: "))
                for r in system.list_reservations(user_id):
                    print(f"{r.id} | {r.user.name} | {r.slot.start_time} - {r.slot.end_time} | {r.status}")
            except ValueError:
                print("Please choose an ID")
        elif choice == 4:
            break


def main():
    system = load_data("data.json")
    print("System loaded")
    run(system)
    save_data(system.reservations, "data.json")


if __name__ == '__main__':
    main()
