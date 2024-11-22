from database_manager import DatabaseManager


class Reporting:
    def __init__(self):
        self.db = DatabaseManager()
        self.db.connect()

    def show_occupied_slots(self):
        query = "SELECT * FROM slots WHERE status = 'occupied';"
        occupied_slots = self.db.fetch_all(query)
        if occupied_slots:
            print("Occupied Slots:")
            for slot in occupied_slots:
                print(f"Slot ID: {slot[0]}, Type: {slot[1]}, Status: {slot[2]}")
        else:
            print("No occupied slots.")

    def show_transaction_history(self):
        query = """
        SELECT vehicles.license_plate, slots.type, transactions.amount, transactions.payment_time
        FROM transactions
        JOIN vehicles ON vehicles.id = transactions.vehicle_id
        JOIN slots ON slots.id = transactions.slot_id;
        """
        transactions = self.db.fetch_all(query)
        if transactions:
            print("Transaction History:")
            for transaction in transactions:
                print(
                    f"Vehicle: {transaction[0]}, Slot Type: {transaction[1]}, Amount: {transaction[2]}, Time: {transaction[3]}")
        else:
            print("No transactions found.")

    def close(self):
        self.db.close()
