# Run multiple database queries concurrently using asyncio.gather.

import asyncio
import aiomysql


# Async function to fetch all users
async def async_fetch_users(pool):
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM users;")
            result = await cur.fetchall()
            print(" All Users:")
            for row in result:
                print(row)
            return result


# Async function to fetch users older than 40
async def async_fetch_older_users(pool):
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM users WHERE age > %s;", (40,))
            result = await cur.fetchall()
            print("\n Users older than 40:")
            for row in result:
                print(row)
            return result


# Run both queries concurrently
async def fetch_concurrently():
    pool = await aiomysql.create_pool(
        host="localhost",
        user="root",
        password="mypassword",
        db="ALX_prodev",
        port=3306
    )

    async with pool:
        results = await asyncio.gather(
            async_fetch_users(pool),
            async_fetch_older_users(pool)
        )
    return results


# Run with asyncio
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
