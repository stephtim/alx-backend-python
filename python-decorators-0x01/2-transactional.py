# decorator that manages database transactions by automatically committing or rolling back changes
import sqlite3
import functools

# --- with_db_connection decorator (from previous task) ---
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # Path to your database
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

# --- transactional decorator ---
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit transaction if no error
            return result
        except Exception as e:
            conn.rollback()  # Rollback on error
            print(f"[ERROR] Transaction failed. Rolled back. Reason: {e}")
            raise
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# --- Update user's email with automatic transaction handling ---
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
print("User email updated successfully!")
