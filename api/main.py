from src.predict import predict_house_price
from fastapi import FastAPI
from pydantic import BaseModel
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI()

class HouseData(BaseModel):
    OverallQual: int
    GrLivArea: float
    TotalBsmtSF: float
    SecondFlrSF: float
    BsmtFinSF1: float
    FirstFlrSF: float
    LotArea: float
    GarageArea: float

@app.get("/")
def home():
    logger.info("Home endpoint accessed.")
    return {"message": "Welcome to the House Price Prediction API!"}

@app.get("/health")
def health():

    logger.info("Health endpoint accessed.")

    return {
        "status": "Healthy"
    }
@app.get("/model-info")
def model_info():

    logger.info("Model information requested.")

    return {
        "Model": "Random Forest Regressor",
        "Preprocessing": "ColumnTransformer + OneHotEncoder",
        "Pipeline": "Loaded",
        "Status": "Ready for Prediction"
         "version": "1.0",
        "created_at": "2026-07-20",
        "metrics": {
            "rmse": 2.5,
            "r2_score": 0.89
        }
    }
@app.post("/predict")
def predict(data: HouseData):

    input_data = {
        "OverallQual": data.OverallQual,
        "GrLivArea": data.GrLivArea,
        "TotalBsmtSF": data.TotalBsmtSF,
        "2ndFlrSF": data.SecondFlrSF,
        "BsmtFinSF1": data.BsmtFinSF1,
        "1stFlrSF": data.FirstFlrSF,
        "LotArea": data.LotArea,
        "GarageArea": data.GarageArea
    }

    logger.info("Prediction request received.")

    prediction = predict_house_price(input_data)

    logger.info(f"Prediction generated: {prediction}")

    return {
        "predicted_price": prediction
    }