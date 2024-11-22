import mysql.connector


class DatabaseManager:
    def __init__(self, host="localhost", user="root", password="", database="parking_lot"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Database connection successful!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.create_database()

    def create_database(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS parking_lot;")
            cursor.execute("USE parking_lot;")

            # Create tables if they don't exist
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS slots (
                id INT AUTO_INCREMENT PRIMARY KEY,
                type VARCHAR(10) NOT NULL,
                status VARCHAR(10) NOT NULL DEFAULT 'available'
            );
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                license_plate VARCHAR(20) NOT NULL,
                type VARCHAR(10) NOT NULL,
                entry_time DATETIME NOT NULL,
                exit_time DATETIME,
                slot_id INT,
                FOREIGN KEY (slot_id) REFERENCES slots(id)
            );
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                vehicle_id INT NOT NULL,
                slot_id INT NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                payment_time DATETIME NOT NULL,
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
                FOREIGN KEY (slot_id) REFERENCES slots(id)
            );
            """)
            connection.commit()
            print("Database and tables created successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def execute_query(self, query, values=None):
        try:
            if self.cursor is None:
                raise Exception("Database connection is not established. Please check the connection.")
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            # Clear any remaining results
            while self.cursor.nextset():
                pass
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        except Exception as e:
            print(f"Error: {e}")

    def fetch_all(self, query, values=None):
        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            results = self.cursor.fetchall()
            # Clear any remaining results
            while self.cursor.nextset():
                pass
            return results
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def fetch_one(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            result = self.cursor.fetchone()
            # Clear any remaining results
            while self.cursor.nextset():
                pass
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def get_last_insert_id(self):
        # Get the last inserted ID from the last executed query
        return self.cursor.lastrowid

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")
