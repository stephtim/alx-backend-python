#!/usr/bin/python3
import mysql.connector

def connect_to_prodev():
    """Connect directly to ALX_prodev database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",         # 🔧 change to your MySQL user
        password="password", # 🔧 change to your MySQL password
        database="ALX_prodev"
    )

def paginate_users(page_size, offset):
    """
    Fetch a single page of users with LIMIT and OFFSET.
    Returns a list of rows.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM user_data ORDER BY user_id LIMIT %s OFFSET %s",
        (page_size, offset)
    )
    rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return rows

def lazy_paginate(page_size):
    """
    Generator that yields pages of users lazily.
    Uses only one loop.
    """
    offset = 0
    while True:  # ✅ only loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

# ------------------------
# Example usage
# ------------------------
if __name__ == "__main__":
    for page in lazy_paginate(5):  # fetch 5 rows at a time
        print("NEW PAGE:")
        for user in page:
            print(user)
