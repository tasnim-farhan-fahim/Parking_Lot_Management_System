from database_manager import DatabaseManager
from datetime import datetime


class Billing:
    def __init__(self):
        self.db = DatabaseManager()
        self.db.connect()

    def calculate_fee(self, entry_time, exit_time, rate_per_hour=20):
        # Convert entry_time to string if it's a datetime object
        if isinstance(entry_time, datetime):
            entry_time_str = entry_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            entry_time_str = entry_time

        # Convert exit_time to string if it's a datetime object
        if isinstance(exit_time, datetime):
            exit_time_str = exit_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            exit_time_str = exit_time

        # Convert to datetime objects and calculate duration
        entry_time_obj = datetime.strptime(entry_time_str, "%Y-%m-%d %H:%M:%S")
        exit_time_obj = datetime.strptime(exit_time_str, "%Y-%m-%d %H:%M:%S")

        duration = (exit_time_obj - entry_time_obj).total_seconds() / 3600  # Convert seconds to hours
        fee = round(duration * rate_per_hour, 2)
        return max(fee, rate_per_hour)  # Ensure minimum fee for first hour

    def log_payment(self, vehicle_id, slot_id, amount):
        query = """
        INSERT INTO transactions (vehicle_id, slot_id, amount, payment_time)
        VALUES (%s, %s, %s, NOW());
        """
        self.db.execute_query(query, (vehicle_id, slot_id, amount))
        print(f"Payment of {amount} logged for vehicle {vehicle_id}.")

    def close(self):
        self.db.close()
