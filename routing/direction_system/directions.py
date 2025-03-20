from typing import List, Tuple
from models import RouteInfo

from routing.global_variables import calculate_geodesic_distance
from routing.direction_system.directions_computation import (
    get_street_name,
    get_cardinal_direction,
    get_turn_direction,
)


def get_directions(G, path, route) -> List[RouteInfo]:
    # Initialize the route information list
    route_info = []
    cumulative_distance = 0

    # Get the street name for the first segment
    current_street = get_street_name(G, path[0], path[1])

    # Iterate over the path to generate route instructions
    for i in range(1, len(path)):
        # Get the street name and distance for the current segment
        new_street = get_street_name(G, path[i - 1], path[i])

        # Calculate the distance for the current segment
        segment_distance = calculate_geodesic_distance(route[i - 1], route[i])

        # Update the cumulative distance
        cumulative_distance += segment_distance

        # Generate the route instruction
        if new_street != current_street or i == len(path) - 1:
            if i == 1:
                # Starting point
                direction = get_cardinal_direction(route[0], route[1])
                instruction = f"Walk {direction} on {current_street}."
            elif i == len(path) - 1:
                # Ending point
                instruction = "You have arrived at your destination."
            else:
                # Intermediate point
                turn = get_turn_direction(
                    route[0], route[i - 2], route[i - 1], route[i]
                )
                instruction = f"{turn} onto {new_street}."

            # Add the route information to the list
            route_info.append(
                RouteInfo(
                    instruction=instruction,
                    distance=round(cumulative_distance, 2),
                )
            )

            # Update the current street and reset the cumulative distance
            current_street = new_street
            cumulative_distance = 0

    return route_info
