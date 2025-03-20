import aiofiles
import os
import json
from shapely.geometry import Polygon
from rtree import index
from routing.global_variables import (
    set_flood_index,
    set_flooded_areas,
)


async def load_flooded_areas():

    dir = "./routing/flood_data"
    files = os.listdir(dir)

    flooded_areas = {}
    flood_index = {}

    for file in files:
        # Parse the data
        async with aiofiles.open(f"{dir}/{file}") as f:
            data = await f.read()
            areas = [
                Polygon([(lat, lng) for lng, lat in area[0]])
                for area in json.loads(data)["features"][0]["geometry"]["coordinates"]
            ]

            # Create R-tree index
            idx = index.Index()
            for i, area in enumerate(areas):
                idx.insert(i, area.bounds)

            # Store the data as a key-value pair
            flooded_areas[file] = areas
            flood_index[file] = idx

    set_flooded_areas(flooded_areas)
    set_flood_index(flood_index)
