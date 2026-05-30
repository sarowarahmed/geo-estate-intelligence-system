import re
import math
from .geo_features import (
    get_distance_to_metro,
    get_geo_features
)

# -----------------------------------
# LOCATION MAP
# -----------------------------------
location_MAP = {
    "new town": "New Town",
    "rajarhat": "Rajarhat",
    "salt lake": "Salt Lake",
    "garia": "Garia",
    "behala": "Behala",
    "vip nagar": "VIP Nagar",
    "chinar park": "Chinar Park",
    "nayabad": "Nayabad",
    "dum dum": "Dum Dum",
    "barasat": "Barasat",
    "howrah": "Howrah",
    "shyambazar": "Shyambazar",
    "beleghata": "Beleghata",
    "intally": "Intally",
    "rash behari avenue": "Rash Behari Avenue",
    "lake market": "Lake Market",
    "jadavpur": "Jadavpur",
    "bijoygarh": "Bijoygarh",
    "tiljala": "Tiljala",
    "kankurgachi": "Kankurgachi",
    "sealdah": "Sealdah",
    "haridevpur": "Haridevpur",
    "sodepur": "Sodepur",
    "sonarpur": "Sonarpur",
    "madhyamgram": "Madhyamgram",
    "belgharia": "Belgharia",
    "barrackpore": "Barrackpore",
    "bidhan nagar": "Bidhan Nagar",
    "tollygunge": "Tollygunge",
    "ballygunge": "Ballygunge",
    "alipore": "Alipore"
}

# -----------------------------------
# PRICE CLEANING
# -----------------------------------
def clean_price(price):

    if not isinstance(price, str):
        return None

    price = price.replace(",", "").strip()

    try:
        if "Cr" in price:
            num = float(re.findall(r"\d+\.?\d*", price)[0])
            return int(num * 10000000)

        elif "Lac" in price:
            num = float(re.findall(r"\d+\.?\d*", price)[0])
            return int(num * 100000)

    except Exception:
        return None

    return None


# -----------------------------------
# AREA EXTRACTION
# -----------------------------------
def extract_sqft(area):

    if not isinstance(area, str):
        return None

    match = re.search(r"(\d+)\s*sqft", area.lower())

    if match:
        return int(match.group(1))

    return None


# -----------------------------------
# LOCATION EXTRACTION
# -----------------------------------
def extract_location(text):

    if not isinstance(text, str):
        return None

    text = text.lower()

    for key, value in location_MAP.items():
        if key in text:
            return value

    return None


# -----------------------------------
# LOCATION SCORE
# -----------------------------------
def get_location_score(location):

    scores = {
        "Alipore": 10,
        "Ballygunge": 10,

        "Salt Lake": 9,
        "New Town": 9,
        "Rash Behari Avenue": 9,
        "Lake Market": 9,

        "Tollygunge": 8,
        "Kankurgachi": 8,
        "Bidhan Nagar": 8,
        "Jadavpur": 8,
        "Beleghata": 8,

        "Rajarhat": 7,
        "Behala": 7,
        "Garia": 7,
        "VIP Nagar": 7,
        "Chinar Park": 7,
        "Shyambazar": 7,
        "Sealdah": 7,

        "Dum Dum": 6,
        "Nayabad": 6,
        "Bijoygarh": 6,
        "Intally": 6,
        "Tiljala": 6,
        "Haridevpur": 6,

        "Barasat": 5,
        "Howrah": 5,
        "Sodepur": 5,
        "Sonarpur": 5,
        "Madhyamgram": 5,
        "Belgharia": 5,
        "Barrackpore": 5,
    }

    return scores.get(location, 4)


# -----------------------------------
# LIVABILITY SCORE
# -----------------------------------
def compute_livability(row):

    distances = [
        row["metro_distance_km"],
        row["railway_distance_km"],
        row["bus_stop_distance_km"],
        row["hospital_distance_km"],
        row["school_distance_km"],
        row["college_distance_km"],
        row["police_distance_km"],
        row["postoffice_distance_km"],
    ]

    distances = [
        d for d in distances
        if d is not None and not math.isnan(d)
    ]

    if not distances:
        return 0

    avg_dist = sum(distances) / len(distances)

    score = 10 * (1 / (1 + avg_dist / 2))

    return round(score, 2)


# -----------------------------------
# MAIN CLEANER
# -----------------------------------
def clean_data(df):

    df["price"] = df["price"].apply(clean_price)
    df["sqft"] = df["area"].apply(extract_sqft)
    df["location"] = df["location_text"].apply(extract_location)

    geo_data = df["location"].apply(get_geo_features)

    geo_df = pd.DataFrame(list(geo_data))

    df = pd.concat(
        [df.reset_index(drop=True),
        geo_df.reset_index(drop=True)],
        axis=1
    )

    # Keep only valid locations
    df = df.dropna(
        subset=[
            "price",
            "sqft",
            "location"
        ]
    )

    # Temporary geo placeholders
#    df["metro_distance_km"] = 5
#    df["hospital_distance_km"] = 5
#    df["school_distance_km"] = 5#
#    df["college_distance_km"] = 5
#    df["bus_stop_distance_km"] = 5
#    df["railway_distance_km"] = 5
#    df["police_distance_km"] = 5
#    df["postoffice_distance_km"] = 5
#
    df["location_score"] = df["location"].apply(
        get_location_score
    )

    df["livability_score"] = df.apply(
        compute_livability,
        axis=1
    )

    print("\nDEBUG LOCATIONS:")
    print(sorted(df["location"].unique()))

    print("\nTOTAL CLEAN ROWS:")
    print(len(df))

    return df


# -----------------------------------
# TEST RUN
# -----------------------------------
if __name__ == "__main__":

    import pandas as pd
    from sqlalchemy import create_engine

    print("Loading data...")

    engine = create_engine(
        "sqlite:///data/real_estate.db"
    )

    df = pd.read_sql(
        "SELECT * FROM properties",
        engine
    )

    print("Raw rows:", len(df))

    df_clean = clean_data(df)

    df_clean.to_sql(
        "properties",
        engine,
        if_exists="replace",
        index=False
    )

    print("Clean rows:", len(df_clean))
    print(df_clean.head())#