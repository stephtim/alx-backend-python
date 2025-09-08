# aiosqlite library to interact with SQLite asynchronously
import asyncio
import aiosqlite


# Async function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("ALX_prodev.db") as db:
        db.row_factory = aiosqlite.Row  # return rows as dictionaries
        async with db.execute("SELECT * FROM users;") as cursor:
            result = await cursor.fetchall()
            print(" All Users:")
            for row in result:
                print(dict(row))
            return result


# Async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("ALX_prodev.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE age > ?;", (40,)) as cursor:
            result = await cursor.fetchall()
            print("\n Users older than 40:")
            for row in result:
                print(dict(row))
            return result


# Run both queries concurrently
async def fetch_concurrently():
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results


# Run with asyncio
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
