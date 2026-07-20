import streamlit as st
import requests

st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="centered"
)

st.sidebar.title("House Price Prediction")

st.sidebar.write(
    """
    **Machine Learning Model**

    - Random Forest Regressor
    - Top 8 Features
    - Scikit-Learn Pipeline
    - FastAPI Backend
    - Streamlit Frontend
    """
)

st.title("🏠 House Price Prediction")

st.write(
    "Enter the details of a house to predict its selling price."
)

overall_qual = st.slider(
    "Overall Quality",
    min_value=1,
    max_value=10,
    value=5
)

gr_liv_area = st.number_input(
    "Ground Living Area (sq ft)",
    min_value=0.0,
    value=1500.0
)

total_bsmt_sf = st.number_input(
    "Total Basement Area (sq ft)",
    min_value=0.0,
    value=800.0
)

second_flr_sf = st.number_input(
    "Second Floor Area (sq ft)",
    min_value=0.0,
    value=500.0
)

bsmt_fin_sf1 = st.number_input(
    "Finished Basement Area (sq ft)",
    min_value=0.0,
    value=400.0
)

first_flr_sf = st.number_input(
    "First Floor Area (sq ft)",
    min_value=0.0,
    value=1000.0
)

lot_area = st.number_input(
    "Lot Area (sq ft)",
    min_value=0.0,
    value=8000.0
)

garage_area = st.number_input(
    "Garage Area (sq ft)",
    min_value=0.0,
    value=500.0
)

if st.button("Predict House Price"):

    input_data = {
        "OverallQual": overall_qual,
        "GrLivArea": gr_liv_area,
        "TotalBsmtSF": total_bsmt_sf,
        "SecondFlrSF": second_flr_sf,
        "BsmtFinSF1": bsmt_fin_sf1,
        "FirstFlrSF": first_flr_sf,
        "LotArea": lot_area,
        "GarageArea": garage_area
    }

    with st.spinner("Predicting..."):

        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=input_data
        )

    if response.status_code == 200:
        predicted_price = response.json()["predicted_price"]

        st.success(
            f"🏠 Predicted House Price: ${predicted_price:,.2f}"
        )

    else:
        st.error("Prediction failed. Please make sure the FastAPI server is running.")