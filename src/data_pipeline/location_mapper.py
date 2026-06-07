from geopy.distance import geodesic

def get_nearest_locations(
    lat,
    lon,
    location_coords,
    top_n=5
):

    clicked = (lat, lon)

    distances = []

    for location, coords in location_coords.items():

        d = geodesic(
            clicked,
            coords
        ).km

        distances.append(
            (
                location,
                round(d, 2)
            )
        )

    distances.sort(
        key=lambda x: x[1]
    )

    return distances[:top_n]