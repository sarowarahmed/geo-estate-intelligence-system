import sys
import os

# Add project root to Python path
root_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_DIR not in sys.path:
    sys.path.append(root_DIR)

import streamlit as st
import pandas as pd
import joblib
import shap
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from sqlalchemy import create_engine
from config.settings import features_PATH, db_PATH, model_PATH
from geopy.geocoders import Nominatim
from src.data_pipeline.geo_osm import get_nearest_places
from streamlit_folium import st_folium
import folium
import pydeck as pdk
from src.data_pipeline.cleaner import get_location_score
from sklearn.metrics.pairwise import euclidean_distances
from geopy.distance import geodesic
from src.data_pipeline.geo_features import locations_COORDS
from src.data_pipeline.geo_features import get_nearest_metro
from src.data_pipeline.location_mapper import (
    get_nearest_locations
)

from src.data_pipeline.geo_features import (
    locations_COORDS
)

def get_nearest_location(lat, lon):

    clicked = (lat, lon)

    nearest_location = None
    nearest_distance = float("inf")

    for location, coords in locations_COORDS.items():

        dist = geodesic(
            clicked,
            coords
        ).km

        if dist < nearest_distance:
            nearest_distance = dist
            nearest_location = location

    return nearest_location

# -----------------------
# CONFIG
# -----------------------
st.set_page_config(layout="wide")
st.title("🏠 AI Real Estate Intelligence System")

# -----------------------
# LOAD MODEL + DATA
# -----------------------
model = joblib.load(model_PATH)
#st.write("Model loaded:", model_PATH)
#st.write(type(model))
#st.write(model)
#st.write("MODEL FEATURES:")
#st.write(model.get_booster().feature_names)
#st.write("N TREES:")
#st.write(model.n_estimators)
#st.write("TEST PREDICTION")

dummy = pd.DataFrame([{
    "sqft":1200,
    "location_score":8,
    "livability_score":5,
    "metro_distance_km":1,
    "hospital_distance_km":1,
    "school_distance_km":1,
    "college_distance_km":1,
    "bus_stop_distance_km":1,
    "railway_distance_km":1,
    "police_distance_km":1,
    "postoffice_distance_km":1
}])

#st.write(model.predict(dummy))
engine = create_engine(db_PATH)
df = pd.read_sql("SELECT * FROM properties", engine)

# -----------------------
# SHAP EXPLAINER
# -----------------------

@st.cache_resource
def load_explainer():
    return shap.Explainer(
        model,
        df[features_PATH]
    )

explainer = load_explainer()

# -----------------------
# GEO SETUP
# -----------------------
geolocator = Nominatim(user_agent="heatmap_app")

@st.cache_data
def get_lat_lon(location):
    try:
        loc = geolocator.geocode(location + ", Kolkata, India")
        return loc.latitude, loc.longitude
    except:
        return None, None

# -----------------------
# HEATMAP DATA
# -----------------------
@st.cache_data
def prepare_intelligence_heatmap(df):

    grouped = (
        df.groupby("location")
        .agg({
            "price": "mean",
            "location_score": "mean",
            "livability_score": "mean",
            "metro_distance_km": "mean"
        })
        .reset_index()
    )

    heatmap_data = []

    for _, row in grouped.iterrows():

        lat, lon = get_lat_lon(row["location"])

        if lat is None:
            continue

        # price normalization
        price_factor = (
            row["price"] -
            heatmap_df["avg_price"].min()
        ) / (
            heatmap_df["avg_price"].max() -
            heatmap_df["avg_price"].min()
        )

        affordability_score = 10 - (price_factor * 10)

        investment_score = (
            row["location_score"] * 0.35 +
            row["livability_score"] * 0.35 +
            (10 - min(row["metro_distance_km"], 10)) * 0.15 +
            affordability_score * 0.15
        )

        if investment_score >= 6.5:
            color = [0, 200, 0, 180]     # Green

        elif investment_score >= 4.5:
            color = [255, 215, 0, 180]   # Yellow

        else:
            color = [220, 0, 0, 180]     # Red

        heatmap_data.append({
            "location": row["location"],
            "lat": lat,
            "lon": lon,
            "avg_price": row["price"],
            "investment_score": round(
                investment_score,
                2
            ),
            "color": color,
            "radius": max(
                40,
                min(
                    investment_score * 35,
                    250
                )
            )
        })


    return pd.DataFrame(heatmap_data)

heatmap_df = prepare_intelligence_heatmap(df)

# -----------------------
# SIDEBAR INPUT
# -----------------------
st.sidebar.header("Enter Property Details")

sqft = st.sidebar.slider("Area (sqft)", 500, 5000, 1200)

st.sidebar.subheader("📍 Select Location")
locations = sorted(df["location"].dropna().unique())
selected_location = st.sidebar.selectbox("Choose Area", locations)

# Auto location score (no manual slider)
selected_location = selected_location.strip()
#location_score = get_location_score(selected_location)

# -----------------------
# MAP SECTION
# -----------------------
st.subheader("🗺️ Click on Map to Predict")

m = folium.Map(location=[22.57, 88.36], zoom_start=12)
map_data = st_folium(m, width=700, height=500)

# -----------------------
# HEATMAP UI
# -----------------------
st.subheader("🌡️ Kolkata Real Estate Intelligence Heatmap")

if not heatmap_df.empty:

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=heatmap_df,
        get_position='[lon, lat]',
        get_radius="radius",
        get_fill_color="color",
        pickable=True
    )

    tooltip = {
        "html": """
        <b>{location}</b><br/>
        Avg Price: ₹{avg_price}<br/>
        Investment Score: {investment_score}
        """
    }

    view_state = pdk.ViewState(
        latitude=22.57,
        longitude=88.36,
        zoom=10
    )

    st.pydeck_chart(
        pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip=tooltip
        )
    )

# =====================================
# Price Formatting
# =====================================

def format_price(price):

    if price >= 10000000:
        return f"₹{price/10000000:.2f} Cr"

    return f"₹{price/100000:.0f} L"


# -----------------------
# TOP INVESTMENT ZONES
# -----------------------
st.subheader("🔥 Top Investment Zones")

top_zones = (
    heatmap_df
    .sort_values(
        "investment_score",
        ascending=False
    )
    .head(10)
)
top_zones = top_zones.copy()
top_zones["avg_price"] = (
    top_zones["avg_price"]
    .apply(format_price)
)
st.dataframe(
    top_zones[
        [
            "location",
            "investment_score",
            "avg_price"
        ]
    ]
)

nearby_areas = []
# -----------------------
# WAIT FOR MAP CLICK
# -----------------------
if not map_data or not map_data.get("last_clicked"):
    st.warning("📍 Click on map to get prediction")

else:
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    nearest_location = get_nearest_location(
        lat,
        lon
    )

    location_score = get_location_score(
        nearest_location
    )

    nearby_areas = get_nearest_locations(
        lat,
        lon,
        locations_COORDS,
        top_n=5
    )

    st.info(
        f"Detected Area: {nearest_location}"
    )

    st.success(f"📍 Selected Location: {lat:.4f}, {lon:.4f}")

    # -----------------------
    # GEO FEATURES
    # -----------------------
    geo_data = get_nearest_places(lat, lon)
    metro_info = get_nearest_metro(lat, lon)

    #st.write("GEO DATA")
    #st.json(geo_data)

    metro_distance = metro_info["metro_distance_km"]
    nearest_metro = metro_info["metro_name"]
    hospital_distance = geo_data.get("hospital", 5)
    school_distance = geo_data.get("school", 5)
    college_distance = geo_data.get("college", 5)
    bus_distance = geo_data.get("bus", 3)
    railway_distance = geo_data.get("railway", 5)
    police_distance = geo_data.get("police", 5)
    postoffice_distance = geo_data.get("post_office", 5)

    livability_score = round(
        10 * (
            1 / (
                1 + (
                    metro_distance +
                    hospital_distance +
                    school_distance +
                    college_distance +
                    bus_distance +
                    railway_distance +
                    police_distance +
                    postoffice_distance
                ) / 8 / 2
            )
        ),
        2
    )
    
    # -----------------------
    # BUILD INPUT
    # -----------------------
    input_data = pd.DataFrame([{
        "sqft": sqft,
        "location_score": location_score,
        "livability_score": livability_score,
        "metro_distance_km": metro_distance,
        "hospital_distance_km": hospital_distance,
        "school_distance_km": school_distance,
        "college_distance_km": college_distance,
        "bus_stop_distance_km": bus_distance,
        "railway_distance_km": railway_distance,
        "police_distance_km": police_distance,
        "postoffice_distance_km": postoffice_distance
    }])

    # -----------------------
    # PREDICTION
    # -----------------------
    raw_pred = model.predict(input_data)[0]
    prediction = np.expm1(raw_pred)

    #st.write("INPUT DATA")
    #st.dataframe(input_data)

    #st.write("RAW PRED:", raw_pred)
    #st.write("FINAL PRED:", prediction)

    st.metric(
        "💰 Predicted Price",
        f"₹{int(prediction):,}"
    )

    # -----------------------
    # MARKET VALUE GAP
    # -----------------------

    similar_props = df[
        (df["location"] == nearest_location)
        &
        (
            abs(df["sqft"] - sqft)
            <= 300
        )
    ]

    if len(similar_props) > 0:

        market_avg = similar_props["price"].mean()

        gap_pct = (
            (
                prediction - market_avg
            ) / market_avg
        ) * 100

        st.subheader(
            "📈 Market Value Analysis"
        )

        st.write(
            f"Area Average Price: ₹{int(market_avg):,}"
        )
        st.write(
            f"Your Predicted Price: ₹{int(prediction):,}"
        )

        if gap_pct < -10:

            st.success(
                f"✅ Appears {abs(gap_pct):.1f}% undervalued"
            )

        elif gap_pct > 10:

            st.error(
                f"⚠ Appears {gap_pct:.1f}% overpriced"
            )

        else:

            st.info(
                f"🟡 Fairly valued ({gap_pct:.1f}%)"
            )
        
        # -----------------------
        # INVESTMENT RATING ENGINE
        # -----------------------
        st.subheader("🏆 Investment Rating")
        rating_score = 0
        # Undervaluation

        if gap_pct < -20:
            rating_score += 3

        elif gap_pct < -10:
            rating_score += 2

        elif gap_pct < 0:
            rating_score += 1

        # Location Quality

        if location_score >= 8:
            rating_score += 2

        elif location_score >= 6:
            rating_score += 1

        # Livability

        if livability_score >= 6:
            rating_score += 2

        elif livability_score >= 4:
            rating_score += 1

        # Metro Connectivity

        if metro_distance <= 2:
            rating_score += 2

        elif metro_distance <= 5:
            rating_score += 1

        if rating_score >= 8:

            stars = "★★★★★"
            verdict = "Excellent Opportunity"

        elif rating_score >= 6:

            stars = "★★★★☆"
            verdict = "Strong Buy"

        elif rating_score >= 4:

            stars = "★★★☆☆"
            verdict = "Fair Investment"

        else:

            stars = "★★☆☆☆"
            verdict = "High Risk"

        st.markdown(
            f"""
        ### {stars}

        ## {verdict}
        """
        )

        st.write("### Why?")

        reasons = []

        if gap_pct < 0:
            reasons.append(
                f"✓ {gap_pct:.1f}% undervalued"
            )

        if location_score >= 8:
            reasons.append(
                "✓ Strong location score"
            )

        if livability_score >= 5:
            reasons.append(
                "✓ Healthy livability score"
            )

        if metro_distance <= 5:
            reasons.append(
                "✓ Good metro connectivity"
            )

        for r in reasons:
            st.write(r)

    # -----------------------
    # SMART RECOMMENDATION ENGINE
    # -----------------------
    from sklearn.metrics.pairwise import euclidean_distances

    feature_cols = [
        "sqft",
        "location_score",
        "livability_score",
        "metro_distance_km",
        "hospital_distance_km",
        "railway_distance_km",
        "bus_stop_distance_km",
        "school_distance_km",
        "college_distance_km",
        "police_distance_km",
        "postoffice_distance_km"
    ]

    # -----------------------
    # FILTER RELEVANT PROPERTIES
    # -----------------------
    df_rec = df[
        df["title"].str.contains(
            "flat|apartment|bhk",
            case=False,
            na=False
        )
    ].copy()

    # Keep only detected area
    candidate_areas = [
        area
        for area, dist
        in nearby_areas[:3]
    ]
    df_rec = df_rec[
        df_rec["location"].isin(candidate_areas)
    ]

    # Remove rows with missing values
    df_rec = df_rec.dropna(subset=feature_cols)

    # -----------------------
    # PRICE FORMATTER
    # -----------------------
    def format_price(price):

        if price >= 10000000:
            return f"₹{price/10000000:.2f} Cr"

        return f"₹{price/100000:.0f} L"

    # -----------------------
    # INVESTMENT OPPORTUNITIES
    # -----------------------
    st.subheader(
        "🏆 Best Nearby Investment Opportunities"
    )

    if len(df_rec) == 0:

        st.warning(
            f"No property listings found for {nearest_location}"
        )

    else:

        # -----------------------
        # WEIGHT DATASET
        # -----------------------
        df_rec_weighted = df_rec.copy()

        df_rec_weighted["sqft"] *= 0.5
        df_rec_weighted["location_score"] *= 2.0
        df_rec_weighted["livability_score"] *= 2.0
        df_rec_weighted["metro_distance_km"] *= 1.5
        df_rec_weighted["hospital_distance_km"] *= 1.2
        df_rec_weighted["college_distance_km"] *= 1.3
        df_rec_weighted["school_distance_km"] *= 1.1
        df_rec_weighted["railway_distance_km"] *= 1.4
        df_rec_weighted["bus_stop_distance_km"] *= 0.8
        df_rec_weighted["police_distance_km"] *= 1.0
        df_rec_weighted["postoffice_distance_km"] *= 0.9

        # -----------------------
        # INPUT VECTOR
        # -----------------------
        input_vector = pd.DataFrame([{
            "sqft": sqft,
            "location_score": location_score,
            "livability_score": livability_score,
            "metro_distance_km": metro_distance,
            "hospital_distance_km": hospital_distance,
            "railway_distance_km": railway_distance,
            "bus_stop_distance_km": bus_distance,
            "school_distance_km": school_distance,
            "college_distance_km": college_distance,
            "police_distance_km": police_distance,
            "postoffice_distance_km": postoffice_distance
        }])

        input_vector["sqft"] *= 0.5
        input_vector["location_score"] *= 2.0
        input_vector["livability_score"] *= 2.0
        input_vector["metro_distance_km"] *= 1.5
        input_vector["hospital_distance_km"] *= 1.2
        input_vector["bus_stop_distance_km"] *= 0.8
        input_vector["railway_distance_km"] *= 1.4
        input_vector["school_distance_km"] *= 1.1
        input_vector["college_distance_km"] *= 1.3
        input_vector["police_distance_km"] *= 1.0
        input_vector["postoffice_distance_km"] *= 0.9

        # -----------------------
        # DISTANCE CALCULATION
        # -----------------------
        distances = euclidean_distances(
            df_rec_weighted[feature_cols],
            input_vector[feature_cols]
        )

        df_rec["similarity"] = distances.flatten()

        recommendations = (
            df_rec
            .sort_values("similarity")
            .head(5)
        )

        # -----------------------
        # DISPLAY PROPERTY CARDS
        # -----------------------
        for idx, row in recommendations.iterrows():

            st.markdown("---")

            title = str(
                row.get(
                    "title",
                    f"Property #{idx}"
                )
            )

            if row["price"] < prediction:
                badge = "🟢 Undervalued"

            elif row["price"] <= prediction * 1.15:
                badge = "🟡 Fair Value"

            else:
                badge = "🔴 Premium"

            st.markdown(
                f"""
    ### 🏠 {title}

    📍 **Location:** {row['location']}

    💰 **Price:** {format_price(row['price'])}

    📐 **Area:** {int(row['sqft'])} sqft

    🌿 **Livability Score:** {row['livability_score']:.1f}/10

    ⭐ **Investment Signal:** {badge}
    """
            )

    # -----------------------
    # CONFIDENCE RANGE
    # -----------------------
    samples = []
    for _ in range(30):
        noisy = input_data.copy()
        noisy["sqft"] *= np.random.uniform(0.9, 1.1)
        samples.append(np.expm1(model.predict(noisy)[0]))

    low = np.percentile(samples, 10)
    high = np.percentile(samples, 90)

    st.write(f"📉 Confidence Range: ₹{int(low):,} - ₹{int(high):,}")

    # -----------------------
    # INFRA DISPLAY
    # -----------------------
    st.subheader("📍 Nearby Infrastructure")
    st.write({
        "🚇 Metro (km)": nearest_metro,
        "🏥 Hospital (km)": hospital_distance,
        "🏫 School (km)": school_distance,
        "🎓 College (km)": college_distance,
        "🚌 Bus Stop (km)": bus_distance,
        "🚆 Railway (km)": railway_distance,
        "🚓 Police (km)": police_distance,
        "🏤 Post Office (km)": postoffice_distance
    })

    st.subheader("🧠 Location Intelligence Report")

    if livability_score >= 8:
        grade = "A+"
    elif livability_score >= 6:
        grade = "A"
    elif livability_score >= 4:
        grade = "B"
    else:
        grade = "C"

    if metro_distance < 1:
        metro_rating = "Excellent"
    elif metro_distance < 3:
        metro_rating = "Good"
    else:
        metro_rating = "Average"

    st.success(f"🏆 Investment Grade: {grade}")
    st.write(f"🌿 Livability Score: {livability_score}/10")
    st.write(f"🚇 Metro Access: {metro_rating}")
    st.write(f"🚇 Nearest Metro: {nearest_metro} ({metro_distance:.2f} km)")
    st.write(f"🏥 Hospital Distance: {hospital_distance:.2f} km")
    st.write(f"🏫 School Access: {school_distance:.2f} km")
    st.write(f"🚆 Railway Distance: {railway_distance:.2f} km")
    st.write(f"🎓 College Access: {college_distance:.2f} km")
    st.write(f"🚌 Bus Stop Distance: {bus_distance:.2f} km")
    st.write(f"🚓 Police Station Distance: {police_distance:.2f} km")
    st.write(f"🏤 Post Office: {postoffice_distance:.2f} km")

    # -----------------------
    # SHAP
    # -----------------------
    st.subheader("🎯 Explainability")

    #explainer = shap.Explainer(model, df[features_PATH])
    sample_df = df[features_PATH].sample(
        min(200, len(df)),
        random_state=42
    )

    shap_values_full = explainer(sample_df)
    shap_values_input = explainer(input_data)

    fig, ax = plt.subplots()
    shap.summary_plot(shap_values_full, sample_df, show=False)
    st.pyplot(fig)

    contributions = shap_values_input[0].values
    feature_names = input_data.columns

    top_features = sorted(
        zip(feature_names, contributions),
        key=lambda x: abs(x[1]),
        reverse=True
    )[:3]

    st.subheader("🎯 Top Reasons")

    total = sum(abs(contributions))

    for name, val in top_features:
        impact = (val / total) * prediction

        if val > 0:
            st.success(f"✅ {name} increased price by ₹{abs(impact):,.0f}")
        else:
            st.error(f"❌ {name} decreased price by ₹{abs(impact):,.0f}")

# -----------------------
# GLOBAL INSIGHTS
# -----------------------
if nearby_areas:

    st.subheader(
        "📊 Nearby Neighborhood Comparison"
    )

    comparison_rows = []

    for area, distance in nearby_areas:

        area_df = df[
            df["location"] == area
        ]

        if len(area_df) == 0:
            continue

        avg_price = area_df["price"].mean()

        comparison_rows.append({
            "Area": area,
            "Distance (km)": round(distance,2),
            "Avg Price": round(avg_price/10000000,2)
        })

    comparison_df = pd.DataFrame(
        comparison_rows
    )

    st.dataframe(comparison_df)

fig = px.histogram(df, x="price", nbins=20, title="Price Distribution")
st.plotly_chart(fig)
