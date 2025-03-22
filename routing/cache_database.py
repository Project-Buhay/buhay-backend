import asyncpg
import json
from pprint import pprint

from db_env import (
    DB_CACHE_NAME,
    DB_CACHE_USER,
    DB_CACHE_PASSWORD,
    DB_CACHE_HOST,
    DB_CACHE_PORT,
    DB_CACHE_TABLE_NAME,
)

from models import Point, TSPOutput

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
    table = "people"
    async with connection_pool.acquire() as connection:
        async with connection.transaction():
            db_data = await connection.fetchrow(
                f"SELECT person_id, access_control FROM {table} WHERE username = $1 AND password = $2",
                username,
                password,
            )
    print(db_data)
    return db_data

async def add_request_row(constituent_id: int, raw_coordinates: list[Point], coordinate_names: list[str]):
    table = "dispatcher_data"
    async with connection_pool.acquire() as connection:
        async with connection.transaction():
            request_id = await connection.fetchval(
                f"INSERT INTO {table} (coordinate_names, constituent_id, rescued, raw_coordinates) VALUES ($1, $2, $3, $4) RETURNING request_id;", 
                json.dumps({"location_names": coordinate_names}),
                constituent_id,
                False,
                json.dumps({"raw_coordinates": raw_coordinates})
            )
    return request_id

# Input is JSON-formatted str
async def add_route_info_row(route_data: dict):
    table = "route_info"
    async with connection_pool.acquire() as connection:
        async with connection.transaction():
            route_id = await connection.fetchval(
                f"INSERT INTO {table} (route_data) VALUES ($1) RETURNING route_id;",
                json.dumps({"routes": route_data})
            )
    return route_id

async def update_route_info_id(request_id: int, route_info_id: int):
    table = "dispatcher_data"
    async with connection_pool.acquire() as connection:
        async with connection.transaction():
            ret = await connection.fetchval(
                f"UPDATE {table} SET route_info_id = $1 WHERE request_id = $2 RETURNING request_id;",
                route_info_id,
                request_id
            )
    return ret

async def route_info(route_id: str):
    table = "route_info"
    async with connection_pool.acquire() as connection:
        async with connection.transaction():
            db_data = await connection.fetch(
                f"SELECT * FROM {table} WHERE route_id = $1",
                route_id,
            )
    return db_data[0]


async def update_rescued_boolean(request_id: str):
    table = "dispatcher_data"
    async with connection_pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute(
                f"UPDATE {table} SET rescued = true WHERE request_id = $1",
                request_id,
            )
    return
