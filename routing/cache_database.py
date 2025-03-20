import asyncpg
import json

from db_env import (
    DB_CACHE_NAME,
    DB_CACHE_USER,
    DB_CACHE_PASSWORD,
    DB_CACHE_HOST,
    DB_CACHE_PORT,
    DB_CACHE_TABLE_NAME,
)

# Global variable for the connection pool
connection_pool = None


async def connect_to_database():
    global connection_pool
    connection_pool = await asyncpg.create_pool(
        database=DB_CACHE_NAME,
        user=DB_CACHE_USER,
        password=DB_CACHE_PASSWORD,
        host=DB_CACHE_HOST,
        port=DB_CACHE_PORT,
    )


async def close_database_connection():
    await connection_pool.close()


async def read_database(hashed_id: str):
    async with connection_pool.acquire() as connection:
        async with connection.transaction():
            db_data = await connection.fetchrow(
                f"SELECT * FROM {DB_CACHE_TABLE_NAME} WHERE id=$1;", hashed_id
            )
            if db_data:
                db_data = db_data[1:][0]
                # convert db_data to json
                db_data = json.loads(db_data)
            else:
                db_data = []
    return db_data


async def write_to_database(hashed_id, route):
    async with connection_pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute(
                f"INSERT INTO {DB_CACHE_TABLE_NAME} (id, route) VALUES ($1, $2);",
                hashed_id,
                route,
            )

async def search_login(username: str, password: str):
    people_table = "people"
    async with connection_pool.acquire() as connection:
        async with connection.transaction():
            db_data = await connection.fetchrow(
                f"SELECT person_id, access_control FROM {people_table} WHERE username = $1 AND password = $2", 
                username, password
            )
    print(db_data)
    return db_data