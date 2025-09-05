#!/usr/bin/python3
import mysql.connector

def connect_to_prodev():
    """Connect directly to ALX_prodev database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",         # change to your MySQL user
        password="password", # change to your MySQL password
        database="ALX_prodev"
    )

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of rows from user_data.
    Each yield returns a list of rows of size batch_size.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:  # loop 1
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """
    Generator that processes each batch to filter users over the age of 25.
    Yields users individually.
    """
    for batch in stream_users_in_batches(batch_size):  # loop 2
        for user in batch:  # loop 3
            if user['age'] > 25:
                yield user

# ------------------------
# Example usage
# ------------------------
if __name__ == "__main__":
    for user in batch_processing(5):
        print(user)

