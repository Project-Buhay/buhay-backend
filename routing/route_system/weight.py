from routing.global_variables import HIGH_EXPOSURE_THRESHOLD, MEDIUM_EXPOSURE_THRESHOLD


def weight_function(u, v, d) -> float:
    # Get the flood risk and length for the edge
    length = d[0].get("length", 1)
    flood_risk = d[0].get("flood_risk", 0)

    # Assign a weight based on the flood exposure length
    flood_exposure_length = length * flood_risk

    if flood_exposure_length > HIGH_EXPOSURE_THRESHOLD:
        return length * 10
    elif flood_exposure_length > MEDIUM_EXPOSURE_THRESHOLD:
        return length * 5
    elif flood_risk > 0:
        return length * 2

    return length
