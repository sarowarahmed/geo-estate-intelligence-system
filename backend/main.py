import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from config.settings import model_PATH
from src.data_pipeline.geo_osm import get_nearest_places
from src.data_pipeline.cleaner import get_location_score

app = FastAPI()

# Load model
model = joblib.load(model_PATH)

# -----------------------
# INPUT SCHEMA
# -----------------------
class PropertyInput(BaseModel):
    sqft: float
    location: str
    lat: float
    lon: float

# -----------------------
# PREDICTION API
# -----------------------
@app.get("/")
def home():
    return {"message": "Real Estate AI API Running 🚀"}

@app.post("/predict")
def predict(data: PropertyInput):

    # Geo features
    geo = get_nearest_places(data.lat, data.lon)

    # Location score
    location_score = get_location_score(data.location)

    livability_score = round(
        10 * (
            1 / (
                1 + (
                    geo.get("metro", 5)
                    + geo.get("hospital", 5)
                    + geo.get("school", 5)
                    + geo.get("college", 5)
                    + geo.get("bus", 3)
                    + geo.get("railway", 5)
                    + geo.get("police", 5)
                    + geo.get("post_office", 5)
                ) / 8 / 2
            )
        ),
        2
    )

    # Build input
    input_df = pd.DataFrame([{
        "sqft": data.sqft,
        "location_score": location_score,
        "livability_score": livability_score,
        "metro_distance_km": geo.get("metro", 5),
        "hospital_distance_km": geo.get("hospital", 5),
        "school_distance_km": geo.get("school", 5),
        "college_distance_km": geo.get("college", 5),
        "bus_stop_distance_km": geo.get("bus", 3),
        "railway_distance_km": geo.get("railway", 5),
        "police_distance_km": geo.get("police", 5),
        "postoffice_distance_km": geo.get("post_office", 5)
    }])

    # Prediction
    raw_pred = model.predict(input_df)[0]
    prediction = np.expm1(raw_pred)

    return {
        "predicted_price": int(prediction),
        "geo_features": geo
    }