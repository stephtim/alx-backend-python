
#!/usr/bin/python3
import mysql.connector
from itertools import islice

def connect_to_prodev():
    """Connect directly to ALX_prodev database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",         # change to your MySQL user
        password="password", # change to your MySQL password
        database="ALX_prodev"
    )

def stream_users():
    """Generator that yields rows from user_data one by one."""
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:   # ✅ only one loop
        yield row

    cursor.close()
    connection.close()

# ------------------------
# Use the generator + islice
# ------------------------
if __name__ == "__main__":
    # iterate over the generator function and print only the first 6 rows
    for user in islice(stream_users(), 6):
        print(user)
