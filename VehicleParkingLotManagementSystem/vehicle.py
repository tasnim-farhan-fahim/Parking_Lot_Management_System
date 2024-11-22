from database_manager import DatabaseManager
from datetime import datetime
from billing import Billing
from parking_slot import ParkingSlot

class Vehicle:
    def __init__(self):
        self.db = DatabaseManager()
        self.db.connect()

    def log_entry(self, license_plate, vehicle_type, slot_id):
        # Check if the slot is available
        query = "SELECT status FROM slots WHERE id = %s;"
        slot_status = self.db.fetch_one(query, (slot_id,))

        if slot_status and slot_status[0] == "available":
            # Log the vehicle entry
            vehicle_query = "INSERT INTO vehicles (license_plate, type) VALUES (%s, %s);"
            self.db.execute_query(vehicle_query, (license_plate, vehicle_type))
            vehicle_id = self.db.get_last_insert_id()  # Get the last inserted vehicle ID

            # Assign the slot to the vehicle
            slot_manager = ParkingSlot()
            slot_manager.assign_slot(slot_id)

            # Log the entry time
            entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry_query = "INSERT INTO vehicles (id, slot_id, entry_time) VALUES (%s, %s, %s);"
            self.db.execute_query(entry_query, (vehicle_id, slot_id, entry_time))
            print(f"Vehicle {license_plate} logged in at {entry_time}.")
        else:
            print(f"Slot {slot_id} is not available for assignment.")

    def log_exit(self, vehicle_id):
        # Log vehicle exit and calculate parking fee
        query = "SELECT slot_id, entry_time FROM vehicles WHERE id = %s AND exit_time IS NULL;"
        vehicle_entry = self.db.fetch_one(query, (vehicle_id,))

        if vehicle_entry:
            slot_id, entry_time = vehicle_entry
            exit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Calculate parking fee (use a function from Billing class)
            billing_manager = Billing()
            fee = billing_manager.calculate_fee(entry_time, exit_time)

            # Log the exit time and fee
            update_query = "UPDATE vehicles SET exit_time = %s, amount = %s WHERE id = %s AND exit_time IS NULL;"
            self.db.execute_query(update_query, (exit_time, fee, vehicle_id))

            # Vacate the slot
            slot_manager = ParkingSlot()
            slot_manager.vacate_slot(slot_id)
            print(f"Vehicle {vehicle_id} exited. Parking fee: {fee}.")
        else:
            print(f"Vehicle {vehicle_id} is not logged in or already exited.")

    def close(self):
        self.db.close()
