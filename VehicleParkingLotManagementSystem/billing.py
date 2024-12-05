from database_manager import DatabaseManager
from datetime import datetime

class Billing:
    def __init__(self):
        self.db = DatabaseManager()
        self.db.connect()

    def calculate_fee(self, exit_time_str, entry_time_str, rate_per_hour=20):
        # Convert string times to datetime objects
        exit_time = datetime.strptime(exit_time_str, "%Y-%m-%d %H:%M:%S")
        entry_time = datetime.strptime(entry_time_str, "%Y-%m-%d %H:%M:%S")

        # Calculate duration in hours
        duration = (exit_time - entry_time).total_seconds() / 3600
        fee = round(duration * rate_per_hour, 2)
        return max(fee, rate_per_hour)  # Ensure minimum fee for the first hour

    def log_payment(self, vehicle_id, slot_id, amount):
        query = """
        INSERT INTO transactions (vehicle_id, slot_id, amount, payment_time)
        VALUES (%s, %s, %s, NOW());
        """
        self.db.execute_query(query, (vehicle_id, slot_id, amount))
        print(f"Payment of {amount} logged for vehicle {vehicle_id}.")

    def close(self):
        self.db.close()
