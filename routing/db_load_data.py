import aiofiles
import os
import psycopg2
from shapely.geometry import Polygon
from rtree import index
import json
from routing.global_variables import (
    set_flood_index,
    set_flooded_areas,
)
from db_env import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, TABLE_NAME

DATABASE_CONFIG = {
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "host": DB_HOST,  # Use your server's hostname or IP
    "port": DB_PORT,  # Default PostgreSQL port
}


async def load_flooded_areas():
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {TABLE_NAME}")

        rows = cursor.fetchall()

        flooded_areas = {}
        flood_index = {}

        for row in rows:
            # Parse the data
            areas = [
                Polygon([(lat, lng) for lng, lat in area[0]])
                for area in row[1]["features"][0]["geometry"]["coordinates"]
            ]
            # Create R-tree index
            idx = index.Index()
            for i, area in enumerate(areas):
                idx.insert(i, area.bounds)

            # Store the data as a key-value pair
            flooded_areas[row[0]] = areas
            flood_index[row[0]] = idx

        set_flooded_areas(flooded_areas)
        set_flood_index(flood_index)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
        if cursor:
            cursor.close()
