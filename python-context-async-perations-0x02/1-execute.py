# reusable context manager 
import mysql.connector

class ExecuteQuery:
    def __init__(self, query, params=None):
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """Open connection and prepare cursor when entering context"""
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mypassword",
            database="ALX_prodev"
        )
        self.cursor = self.connection.cursor(dictionary=True)
        print("Connected to database.")

        # Execute query immediately
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()  # return query results directly

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up connection and cursor when exiting"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connection closed.")

        if exc_type:
            print(f"Exception occurred: {exc_val}")
        return False  # re-raise exceptions if any


#  Usage
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > %s"
    params = (25,)  # parameterized value

    with ExecuteQuery(query, params) as results:
        print(" Users older than 25:")
        for row in results:
            print(row)
