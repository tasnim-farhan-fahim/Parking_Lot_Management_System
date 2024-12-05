from database_manager import DatabaseManager


class ParkingSlot:
    def __init__(self):
        self.db = DatabaseManager()
        self.db.connect()

    def add_new_slot(self):
        slot_type = input("Select slot type (Car, Bike): ")
        query = ("INSERT INTO slots (type, status) "
                 "VALUES (%s, 'available');")
        self.db.execute_query(query, (slot_type,))
        print(f"New {slot_type} slot added.")

    def view_available_slots(self):
        slot_type = input("Enter the type of slot type (Car, Bike): ")
        query = ("SELECT id "
                 "FROM slots "
                 "WHERE type = %s AND status = 'available';")
        available_slots = self.db.fetch_all(query, (slot_type,))
        if available_slots:
            print("Available slots:")
            for slot in available_slots:
                print(f"Slot ID: {slot[0]}")
        else:
            print("No available slots for this type.")

    def assign_slot_to_vehicle(self):
        # Prompt for slot ID and vehicle ID
        slot_id = int(input("Enter the slot ID to assign: "))
        # Check if the slot exists and is available
        slot_query = "SELECT status FROM slots WHERE id = %s;"
        slot_status = self.db.fetch_one(slot_query, (slot_id,))

        if not slot_status:
            print(f"Slot with ID {slot_id} does not exist.")
            return  # Exit if the slot doesn't exist

        if slot_status[0] == 'occupied':
            print(f"Slot {slot_id} is already occupied.")
            return  # Exit the function if the slot is occupied

        vehicle_id = int(input("Enter the vehicle ID to assign to this slot: "))

        # Check if the vehicle exists in the database
        vehicle_query = "SELECT id FROM vehicles WHERE id = %s;"
        vehicle_entry = self.db.fetch_one(vehicle_query, (vehicle_id,))

        if not vehicle_entry:
            print(f"Vehicle with ID {vehicle_id} does not exist.")
            return  # Exit the function if the vehicle does not exist

        # Proceed to assign the slot to the vehicle
        query = ("UPDATE vehicles "
                 "SET slot_id = %s "
                 "WHERE id = %s;")
        self.db.execute_query(query, (slot_id, vehicle_id))

        # Update slot status to 'occupied'
        query = ("UPDATE slots "
                 "SET status = 'occupied' "
                 "WHERE id = %s;")
        self.db.execute_query(query, (slot_id,))

        print(f"Vehicle {vehicle_id} assigned to Slot {slot_id}.")

    def vacate_slot(self):
        # Prompt for slot ID
        slot_id = int(input("Enter the slot ID to vacate: "))

        # Check if the slot exists
        slot_query = "SELECT status FROM slots WHERE id = %s;"
        slot_status = self.db.fetch_one(slot_query, (slot_id,))

        if not slot_status:
            print(f"Slot with ID {slot_id} does not exist.")
            return  # Exit if the slot doesn't exist

        if slot_status[0] == 'available':
            print(f"Slot {slot_id} is already available.")
            return  # Exit the function if the slot is available

        # Proceed to vacate the slot
        query = ("UPDATE slots "
                 "SET status = 'available' "
                 "WHERE id = %s;")
        self.db.execute_query(query, (slot_id,))

        # Optionally, clear any vehicle associated with this slot
        clear_vehicle_query = ("UPDATE vehicles "
                               "SET slot_id = NULL "
                               "WHERE slot_id = %s;")
        self.db.execute_query(clear_vehicle_query, (slot_id,))

        print(f"Slot {slot_id} has been vacated.")

    def close(self):
        self.db.close()
