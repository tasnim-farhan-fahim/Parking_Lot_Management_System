from database_manager import DatabaseManager
from datetime import datetime
from billing import Billing
from parking_slot import ParkingSlot


class Vehicle:
    def __init__(self):
        self.db = DatabaseManager()
        self.db.connect()


    def entry_vehicle(self):

        license_plate = input("Enter the vehicle license plate: ")
        vehicle_type = input("Enter vehicle type (Car, Bike): ")
        slot_id = int(input("Enter Slot to park vehicle: "))

        query = ("SELECT slots.status "
                 "FROM slots "
                 "WHERE id = %s;")
        slot_status = self.db.fetch_one(query, (slot_id,))

        if slot_status and slot_status[0] == "available":
            # Log vehicle entry
            entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            vehicle_query = ("INSERT INTO vehicles (license_plate, type, entry_time, slot_id) "
                             "VALUES (%s, %s, %s, %s);")
            self.db.execute_query(vehicle_query, (license_plate, vehicle_type, entry_time, slot_id))
            print(f"Vehicle {license_plate} logged in at {entry_time}.")
            query = ("UPDATE slots "
                     "SET status = 'occupied' "
                     "WHERE id = %s;")
            self.db.execute_query(query, (slot_id,))
        else:
            print(f"Slot {slot_id} is not available for assignment.")

    def exit_vehicle(self):
        vehicle_id = input("Enter the vehicle ID to exit: ")

        # Check if the vehicle exists in the database
        vehicle_query = ("SELECT slot_id, entry_time "
                         "FROM vehicles "
                         "WHERE id = %s;")
        vehicle_data = self.db.fetch_one(vehicle_query, (vehicle_id,))

        if vehicle_data:
            slot_id, entry_time = vehicle_data  # `entry_time` is a datetime object

            # Calculate the exit time
            exit_time = datetime.now()

            # Convert entry and exit times to strings for `calculate_fee`
            entry_time_str = entry_time.strftime("%Y-%m-%d %H:%M:%S")
            exit_time_str = exit_time.strftime("%Y-%m-%d %H:%M:%S")

            # Create an instance of Billing
            billing = Billing()

            # Calculate parking fee
            fee = billing.calculate_fee(entry_time_str, exit_time_str)

            # Log payment
            billing.log_payment(vehicle_id, slot_id, fee)

            # Log vehicle exit
            print(f"Vehicle {vehicle_id} exited. Total parked duration: {fee / 20:.2f} hours.")
            print(f"Total fee: {fee:.2f}.")

            # Remove vehicle from database
            update_vehicle_query = """
                    UPDATE vehicles
                    SET exit_time = %s
                    WHERE id = %s;
                    """
            self.db.execute_query(update_vehicle_query, (exit_time_str, vehicle_id))

            # Update slot status to available
            update_slot_query = ("UPDATE slots "
                                 "SET status = 'available' "
                                 "WHERE id = %s;")
            self.db.execute_query(update_slot_query, (slot_id,))

            # Close the Billing instance
            billing.close()

        else:
            print(f"Vehicle with ID {vehicle_id} not found.")

    def close(self):
        self.db.close()
