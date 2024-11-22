from database_manager import DatabaseManager


class ParkingSlot:
    def __init__(self):
        self.db = DatabaseManager()
        self.db.connect()

    def add_slot(self, slot_type):
        # Add a new slot with status 'available'
        query = "INSERT INTO slots (type, status) VALUES (%s, 'available');"
        self.db.execute_query(query, (slot_type,))
        print(f"New {slot_type} slot added.")

    def get_available_slots(self, slot_type):
        # Fetch available slots for a specific type
        query = "SELECT id FROM slots WHERE type = %s AND status = 'available';"
        available_slots = self.db.fetch_all(query, (slot_type,))
        return [slot[0] for slot in available_slots]

    def assign_slot(self, slot_id):
        # Check if the slot is already occupied
        query = "SELECT status FROM slots WHERE id = %s;"
        slot_status = self.db.fetch_one(query, (slot_id,))

        if slot_status and slot_status[0] == "occupied":
            print(f"Slot {slot_id} is already occupied. Please choose another slot.")
        else:
            # Assign the slot by updating its status to 'occupied'
            update_query = "UPDATE slots SET status = 'occupied' WHERE id = %s;"
            self.db.execute_query(update_query, (slot_id,))
            print(f"Slot {slot_id} has been assigned and marked as occupied.")

    def vacate_slot(self, slot_id):
        # Check if the slot is already vacant
        query = "SELECT status FROM slots WHERE id = %s;"
        slot_status = self.db.fetch_one(query, (slot_id,))

        if slot_status and slot_status[0] == "available":
            print(f"Slot {slot_id} is already vacant. There's no need to vacate it.")
        else:
            # Vacate the slot by updating its status to 'available'
            update_query = "UPDATE slots SET status = 'available' WHERE id = %s;"
            self.db.execute_query(update_query, (slot_id,))
            print(f"Slot {slot_id} has been vacated and marked as available.")

    def close(self):
        self.db.close()
