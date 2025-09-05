#!/usr/bin/python3
import mysql.connector

def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",          # 🔧 change if needed
        password="password",  # 🔧 change if needed
        database="ALX_prodev"
    )

def stream_user_ages():
    """
    Generator that yields user ages one by one.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor()

    cursor.execute("SELECT age FROM user_data;")
    for (age,) in cursor:   # ✅ loop 1
        yield age

    cursor.close()
    connection.close()

def calculate_average_age():
    """
    Calculate the average age using the generator
    without loading the full dataset into memory.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():  # ✅ loop 2
        total_age += age
        count += 1

    avg_age = total_age / count if count > 0 else 0
    print(f"Average age of users: {avg_age:.2f}")

# -------------------
# Run the script
# -------------------
if __name__ == "__main__":
    calculate_average_age()
