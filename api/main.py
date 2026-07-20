from src.predict import predict_house_price
from fastapi import FastAPI
from pydantic import BaseModel

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
    return {"message": "Welcome to the House Price Prediction API!"}
@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }
@app.get("/model-info")
def model_info():

    return {
        "Model": "Random Forest Regressor",
        "Preprocessing": "ColumnTransformer + OneHotEncoder",
        "Pipeline": "Loaded",
        "Status": "Ready for Prediction"
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

    prediction = predict_house_price(input_data)

    return {
        "predicted_price": prediction
    }