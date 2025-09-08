# class custom context manager
import mysql.connector

class DatabaseConnection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """Establish database connection when entering context"""
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor(dictionary=True)
        print("Database connection established.")
        return self.cursor  # Return cursor for executing queries

    def __exit__(self, exc_type, exc_value, traceback):
        """Close connection gracefully when exiting context"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")

        # Handle exceptions (optional)
        if exc_type:
            print(f"Exception occurred: {exc_value}")
        # Returning False will propagate exceptions; True would suppress them
        return False


# perfomring the query SELECT * FROM users
import mysql.connector

class DatabaseConnection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """Establish database connection when entering context"""
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor(dictionary=True)
        print("Database connection established.")
        return self.cursor  # return cursor so we can execute queries

    def __exit__(self, exc_type, exc_value, traceback):
        """Close connection gracefully when exiting context"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")

        if exc_type:
            print(f"Exception occurred: {exc_value}")
        return False  # Propagate exception if any


# ✅ Usage of the context manager
if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "mypassword",
        "database": "ALX_prodev"
    }

    with DatabaseConnection(**db_config) as cursor:
        cursor.execute("SELECT * FROM users;")
        results = cursor.fetchall()
        print("Query Results:")
        for row in results:
            print(row)

