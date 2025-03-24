from fastapi import APIRouter, HTTPException, status

from models import SaveRouteInput
from routing.cache_database import add_route_info_row, update_route_info_id
from tsp_endpoint.tsp import tsp
import googlemaps
from db_env import GOOGLE_MAPS_API

router = APIRouter()
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API)

@router.post("/save_route", status_code=status.HTTP_200_OK)
async def save_route(input: SaveRouteInput):
    try:
        tsp_output = await tsp(input.points)
        t = len(tsp_output)
        for i in range(t):
            start_lng, start_lat = tsp_output[i]["start"][0], tsp_output[i]["start"][1]
            end_lng, end_lat = tsp_output[i]["end"][0], tsp_output[i]["end"][1]
            start_name = (gmaps.reverse_geocode((start_lat, start_lng), 
                result_type="street_address|plus_code|premise|establishment|point_of_interest")
                [0]["formatted_address"])
            end_name = (gmaps.reverse_geocode((end_lat, end_lng), 
                result_type="street_address|plus_code|premise|establishment|point_of_interest")
                [0]["formatted_address"])
            tsp_output[i]["start"] = start_name
            tsp_output[i]["end"] = end_name
            tsp_output[i]["data"] = tsp_output[i]["data"].dict()

        route_id = await add_route_info_row(tsp_output)
        success = await update_route_info_id(input.request_id, route_id)
        return {"success": (True if success is not None and success == input.request_id else False)}
    except Exception as e:
        print(f"Error {e}")
        return {"success": 0}