# from database_manager import DatabaseManager
#
#
# def main():
#     db_manager = DatabaseManager()
#     db_manager.connect()
#
#     # Fetch tables
#     tables = db_manager.fetch_all("SHOW TABLES;")
#     print("Tables in the database:", tables)
#
#     # Run another query safely
#     db_manager.execute_query("SELECT * FROM slots;")
#
#     db_manager.close()
#
#
# if __name__ == "__main__":
#     main()
#------------------------------------------------------------------------------
# from parking_slot import ParkingSlot
# from vehicle import Vehicle
#
# def main():
#     # Initialize classes
#     slot_manager = ParkingSlot()
#     vehicle_manager = Vehicle()
#
#     # Add new parking slots
#     slot_manager.add_slot("car")
#     slot_manager.add_slot("bike")
#
#     # Get available slots
#     available_slots = slot_manager.get_available_slots("car")
#     print("Available car slots:", available_slots)
#
#     # Assign a slot and log vehicle entry
#     if available_slots:
#         slot_id = available_slots[0][0]  # Get the first available slot ID
#         slot_manager.assign_slot(slot_id)
#         vehicle_manager.log_entry("ABC123", "car", slot_id)
#
#     # Get vehicle details
#     vehicle_details = vehicle_manager.get_vehicle_details("ABC123")
#     print("Vehicle details:", vehicle_details)
#
#     # Release the slot and log vehicle exit
#     if vehicle_details:
#         vehicle_id = vehicle_details[0][0]
#         vehicle_manager.log_exit(vehicle_id)
#         slot_manager.release_slot(slot_id)
#
#     # Close connections
#     slot_manager.close()
#     vehicle_manager.close()
#
# if __name__ == "__main__":
#     main()
# ------------------------------------------------------------------------
# from parking_slot import ParkingSlot
# from vehicle import Vehicle
# from billing import Billing
# from datetime import datetime  # Import added
#
#
# def main():
#     # Initialize classes
#     slot_manager = ParkingSlot()
#     vehicle_manager = Vehicle()
#     billing_manager = Billing()
#
#     # Add parking slots
#     slot_manager.add_slot("car")
#     slot_manager.add_slot("bike")
#
#     # Get available slots
#     available_slots = slot_manager.get_available_slots("car")
#     print("Available car slots:", available_slots)
#
#     # Assign a slot and log vehicle entry
#     if available_slots:
#         slot_id = available_slots[0][0]  # First available slot ID
#         slot_manager.assign_slot(slot_id)
#         vehicle_manager.log_entry("XYZ789", "car", slot_id)
#
#     # Simulate vehicle exit
#     vehicle_details = vehicle_manager.get_vehicle_details("XYZ789")
#     if vehicle_details:
#         vehicle_id = vehicle_details[0][0]
#         entry_time = vehicle_details[0][3]  # Entry time
#         exit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Simulate exit time
#
#         # Log exit
#         vehicle_manager.log_exit(vehicle_id)
#         slot_manager.release_slot(slot_id)
#
#         # Calculate fee and log payment
#         fee = billing_manager.calculate_fee(entry_time, exit_time)
#         billing_manager.log_payment(vehicle_id, slot_id, fee)
#
#     # Close connections
#     slot_manager.close()
#     vehicle_manager.close()
#     billing_manager.close()
#
#
# if __name__ == "__main__":
#     main()
# ------------------------------------------------------------------------------
# from parking_slot import ParkingSlot
# from vehicle import Vehicle
# from billing import Billing
# from reporting import Reporting
# from datetime import datetime
#
#
# def main():
#     # Initialize classes
#     slot_manager = ParkingSlot()
#     vehicle_manager = Vehicle()
#     billing_manager = Billing()
#     reporting_manager = Reporting()
#
#     while True:
#         print("\n--- Vehicle Parking System ---")
#         print("1. Add Slot")
#         print("2. Get Available Slots")
#         print("3. Assign Slot")
#         print("4. Log Vehicle Entry")
#         print("5. Log Vehicle Exit")
#         print("6. View Occupied Slots")
#         print("7. View Transaction History")
#         print("8. Exit")
#
#         choice = input("Enter your choice: ")
#
#         if choice == "1":
#             slot_type = input("Enter slot type (car/bike): ")
#             slot_manager.add_slot(slot_type)
#         elif choice == "2":
#             slot_type = input("Enter slot type (car/bike): ")
#             available_slots = slot_manager.get_available_slots(slot_type)
#             print("Available slots:", available_slots)
#         elif choice == "3":
#             slot_id = int(input("Enter slot ID to assign: "))
#             slot_manager.assign_slot(slot_id)
#         elif choice == "4":
#             license_plate = input("Enter vehicle license plate: ")
#             vehicle_type = input("Enter vehicle type (car/bike): ")
#             slot_id = int(input("Enter assigned slot ID: "))
#             vehicle_manager.log_entry(license_plate, vehicle_type, slot_id)
#         elif choice == "5":
#             vehicle_id = int(input("Enter vehicle ID to log exit: "))
#             vehicle_manager.log_exit(vehicle_id)
#         elif choice == "6":
#             reporting_manager.show_occupied_slots()
#         elif choice == "7":
#             reporting_manager.show_transaction_history()
#         elif choice == "8":
#             print("Exiting system.")
#             break
#         else:
#             print("Invalid choice. Please try again.")
#
#     # Close all connections before exiting
#     slot_manager.close()
#     vehicle_manager.close()
#     billing_manager.close()
#     reporting_manager.close()
#
#
# if __name__ == "__main__":
#     main()
# -----------------------------------------------------------------------
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
        print("1. Add New Slot")
        print("2. View Available Slots")
        print("3. Assign Slot")
        print("4. Vacate Slot")
        print("5. Entry Vehicle ")
        print("6. Exit Vehicle ")
        print("7. View Occupied Slots")
        print("8. View Transaction History")
        print("9. Exit")

        choice = input("Enter your choice: ")
        # -----------------------------------------------------------------------
        if choice == "1":
            slot_type = input("Enter slot type (car/bike): ")
            if slot_type in ["car", "bike"]:
                slot_manager.add_slot(slot_type)
            else:
                print("Invalid slot type. Please enter 'car' or 'bike'.")

        # -----------------------------------------------------------------------
        elif choice == "2":
            slot_type = input("Enter slot type (car/bike): ")
            if slot_type in ["car", "bike"]:
                available_slots = slot_manager.get_available_slots(slot_type)
                print("Available slots:", available_slots)
            else:
                print("Invalid slot type. Please enter 'car' or 'bike'.")

        # -----------------------------------------------------------------------
        elif choice == "3":
            slot_id = input("Enter slot ID to assign: ")
            try:
                slot_id = int(slot_id)
                slot_manager.assign_slot(slot_id)
            except ValueError:
                print("Please enter a valid slot ID (integer).")
        # -----------------------------------------------------------------------
        elif choice == "4":
            slot_id = input("Enter slot ID to vacate: ")
            try:
                slot_id = int(slot_id)
                slot_manager.vacate_slot(slot_id)
            except ValueError:
                print("Please enter a valid slot ID (integer).")
        # -----------------------------------------------------------------------
        elif choice == "5":
            license_plate = input("Enter vehicle license plate: ")
            if validate_license_plate(license_plate):
                vehicle_type = input("Enter vehicle type (car/bike): ")
                if vehicle_type in ["car", "bike"]:
                    slot_id = input("Enter assigned slot ID: ")
                    try:
                        slot_id = int(slot_id)
                        vehicle_manager.log_entry(license_plate, vehicle_type, slot_id)
                    except ValueError:
                        print("Please enter a valid slot ID (integer).")
                else:
                    print("Invalid vehicle type. Please enter 'car' or 'bike'.")
            else:
                print("Invalid license plate format! Please enter a valid plate.")
        # -----------------------------------------------------------------------
        elif choice == "6":
            vehicle_id = input("Enter vehicle ID to log exit: ")
            try:
                vehicle_id = int(vehicle_id)
                vehicle_manager.log_exit(vehicle_id)
            except ValueError:
                print("Please enter a valid vehicle ID (integer).")
        # -----------------------------------------------------------------------
        elif choice == "7":
            reporting_manager.show_occupied_slots()
        # -----------------------------------------------------------------------
        elif choice == "8":
            reporting_manager.show_transaction_history()
        # -----------------------------------------------------------------------
        elif choice == "9":
            print("Exiting system.")
            break
        # -----------------------------------------------------------------------
        else:
            print("Invalid choice. Please try again.")

    # Close all connections before exiting
    slot_manager.close()
    vehicle_manager.close()
    billing_manager.close()
    reporting_manager.close()


def validate_license_plate(license_plate):
    # Example pattern: only alphanumeric with 1-7 characters
    pattern = r"^[A-Za-z0-9]{1,8}$"
    return bool(re.match(pattern, license_plate))


if __name__ == "__main__":
    main()
