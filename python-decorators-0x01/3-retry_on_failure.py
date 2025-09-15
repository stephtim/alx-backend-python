# decorator thatretrie database operations if they fail due to transient errors
import time
import sqlite3
import functools

# --- with_db_connection decorator ---
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("example.db")  # change to your DB file path
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

# --- retry_on_failure decorator ---
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt < retries:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
            # If all retries fail, raise the last encountered exception
            raise last_exception
        return wrapper
    return decorator

# --- function using both decorators ---
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# --- attempt to fetch users with automatic retry on failure ---
users = fetch_users_with_retry()
print(users)
