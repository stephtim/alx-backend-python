# decorator that logs database queries executed by any function
import sqlite3
import functools

# --- decorator to log SQL queries ---
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Try to get query from positional or keyword arguments
        if 'query' in kwargs:
            query = kwargs['query']
        elif len(args) > 0:
            query = args[0]
        else:
            query = "<NO QUERY FOUND>"
        
        print(f"[LOG] Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# --- fetch users while logging the query ---
users = fetch_all_users(query="SELECT * FROM users")
print(users)
