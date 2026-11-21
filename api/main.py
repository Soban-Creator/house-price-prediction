"""FastAPI backend for the HomeValue AI house price prediction system."""

import logging
import math

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.predict import predict_house_price

# --------------------------------------------------
# Logging configuration
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="HomeValue AI - House Price Prediction API",
    description=(
        "Machine learning API for estimating residential "
        "property prices using a trained Random Forest model."
    ),
    version="1.0.0",
)


# --------------------------------------------------
# Input validation
# --------------------------------------------------

class HouseData(BaseModel):
    """Validate the eight property features required for prediction."""

    OverallQual: int = Field(
        ...,
        ge=1,
        le=10,
        description="Overall material and finish quality (1-10)",
    )

    GrLivArea: float = Field(
        ...,
        gt=0,
        allow_inf_nan=False,
        description="Above-ground living area in square feet",
    )

    TotalBsmtSF: float = Field(
        ...,
        ge=0,
        allow_inf_nan=False,
        description="Total basement area in square feet",
    )

    SecondFlrSF: float = Field(
        ...,
        ge=0,
        allow_inf_nan=False,
        description="Second-floor area in square feet",
    )

    BsmtFinSF1: float = Field(
        ...,
        ge=0,
        allow_inf_nan=False,
        description="Type 1 finished basement area",
    )

    FirstFlrSF: float = Field(
        ...,
        gt=0,
        allow_inf_nan=False,
        description="First-floor area in square feet",
    )

    LotArea: float = Field(
        ...,
        gt=0,
        allow_inf_nan=False,
        description="Lot size in square feet",
    )

    GarageArea: float = Field(
        ...,
        ge=0,
        allow_inf_nan=False,
        description="Garage area in square feet",
    )


# --------------------------------------------------
# Home endpoint
# --------------------------------------------------

@app.get("/")
def home():
    """Return the API welcome message."""
    logger.info("Home endpoint accessed.")

    return {
        "message": "Welcome to the House Price Prediction API!"
    }


# --------------------------------------------------
# Health endpoint
# --------------------------------------------------

@app.get("/health")
def health():
    """Return the API health status."""
    logger.info("Health endpoint accessed.")

    return {
        "status": "Healthy"
    }


# --------------------------------------------------
# Model information endpoint
# --------------------------------------------------

@app.get("/model-info")
def model_info():
    """Return information about the production prediction pipeline."""
    logger.info("Model information requested.")

    return {
        "Model": "Random Forest Regressor",
        "Preprocessing": "ColumnTransformer (8 numerical features passed through)",
        "Pipeline": "Loaded",
        "Status": "Ready for Prediction",
    }


# --------------------------------------------------
# House price prediction endpoint
# --------------------------------------------------

@app.post("/predict")
def predict(data: HouseData):
    """Validate property data and return an estimated house price."""
    logger.info("Prediction request received.")

    # Convert API field names into the feature names
    # expected by the trained machine learning model.
    input_data = {
        "OverallQual": data.OverallQual,
        "GrLivArea": data.GrLivArea,
        "TotalBsmtSF": data.TotalBsmtSF,
        "2ndFlrSF": data.SecondFlrSF,
        "BsmtFinSF1": data.BsmtFinSF1,
        "1stFlrSF": data.FirstFlrSF,
        "LotArea": data.LotArea,
        "GarageArea": data.GarageArea,
    }

    try:
        prediction = float(
            predict_house_price(input_data)
        )

        # Prevent invalid prediction results from
        # being returned to the frontend.
        if not math.isfinite(prediction) or prediction <= 0:
            raise ValueError("Model returned an invalid price.")

    except Exception as exc:
        logger.exception("House price prediction failed.")

        raise HTTPException(
            status_code=500,
            detail="Unable to generate a house price prediction.",
        ) from exc

    logger.info("Prediction completed successfully.")

    return {
        "predicted_price": prediction
    }