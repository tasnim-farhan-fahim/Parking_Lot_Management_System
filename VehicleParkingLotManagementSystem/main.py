import re
from parking_slot import ParkingSlot
from vehicle import Vehicle
from billing import Billing
from reporting import Reporting
from datetime import datetime

def main():
    # Initialize classes
    slot_manager = ParkingSlot()
    vehicle_manager = Vehicle()
    billing_manager = Billing()
    reporting_manager = Reporting()

    while True:
        print("\n--- Vehicle Parking System ---")
        print("1. Add New Slot %")
        print("2. View Available Slots %")
        print("3. Assign Slot %")
        print("4. Vacate Slot %")
        print("5. Entry Vehicle %")
        print("6. Exit Vehicle")
        print("7. View Occupied Slots %")
        print("8. View Transaction History")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            slot_manager.add_new_slot()
        elif choice == "2":
            slot_manager.view_available_slots()
        elif choice == "3":
            slot_manager.assign_slot_to_vehicle()
        elif choice == "4":
            slot_manager.vacate_slot()
        elif choice == "5":
            vehicle_manager.entry_vehicle()
        elif choice == "6":
            vehicle_manager.exit_vehicle()
        elif choice == "7":
            reporting_manager.show_occupied_slots()
        elif choice == "8":
            reporting_manager.show_transaction_history()
        elif choice == "9":
            print("Exiting system.")
            break
        else:
            print("Invalid choice. Please try again.")

    # Close all connections before exiting
    slot_manager.close()
    vehicle_manager.close()
    billing_manager.close()
    reporting_manager.close()

if __name__ == "__main__":
    main()