from typing import List


def create_geojson(route_coordinates: List[List[float]]) -> dict:
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": route_coordinates,
                },
                "properties": {},
            }
        ],
    }
