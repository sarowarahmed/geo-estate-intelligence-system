import osmnx as ox
from geopy.distance import geodesic
from functools import lru_cache


# ----------------------------------
# CONFIG
# ----------------------------------

SEARCH_RADIUS = 3000  # meters


# ----------------------------------
# FETCH NEARBY OSM OBJECTS
# ----------------------------------

@lru_cache(maxsize=500)
def fetch_places(lat, lon, tag_key, tag_value):
    """
    Fetch nearby OSM locations
    """

    try:
        tags = {tag_key: tag_value}

        gdf = ox.features_from_point(
            (lat, lon),
            tags=tags,
            dist=SEARCH_RADIUS
        )

        points = []

        for _, row in gdf.iterrows():

            geom = row.geometry

            if geom is None:
                continue

            if geom.geom_type == "Point":
                points.append(
                    (geom.y, geom.x)
                )

            elif geom.centroid:
                points.append(
                    (geom.centroid.y, geom.centroid.x)
                )

        return points

    except Exception:
        return []


# ----------------------------------
# DISTANCE TO NEAREST LOCATION
# ----------------------------------

def get_distance(origin, tag_key, tag_value):

    lat, lon = origin

    places = fetch_places(
        lat,
        lon,
        tag_key,
        tag_value
    )

    if not places:
        return 5.0

    min_dist = min(
        geodesic(
            (lat, lon),
            place
        ).km
        for place in places
    )

    return round(min_dist, 2)


# ----------------------------------
# MAIN FUNCTION
# ----------------------------------

@lru_cache(maxsize=500)
def get_nearest_places(lat, lon):
    """
    Returns real infrastructure distances
    from OpenStreetMap
    """

    origin = (lat, lon)

    return {

        # Public Transport
        "metro":
            get_distance(
                origin,
                "station",
                "subway"
            ),

        "railway":
            get_distance(
                origin,
                "railway",
                "station"
            ),

        "bus":
            get_distance(
                origin,
                "highway",
                "bus_stop"
            ),

        # Education
        "school":
            get_distance(
                origin,
                "amenity",
                "school"
            ),

        "college":
            get_distance(
                origin,
                "amenity",
                "college"
            ),

        # Healthcare
        "hospital":
            get_distance(
                origin,
                "amenity",
                "hospital"
            ),

        # Public Services
        "police":
            get_distance(
                origin,
                "amenity",
                "police"
            ),

        "post_office":
            get_distance(
                origin,
                "amenity",
                "post_office"
            )
    }