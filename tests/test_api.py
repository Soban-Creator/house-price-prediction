from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_home():

    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Welcome to the House Price Prediction API!"
    }


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "Healthy"
    }


def test_model_info():

    response = client.get("/model-info")

    assert response.status_code == 200

    data = response.json()

    assert data["Model"] == "Random Forest Regressor"
    assert data["Preprocessing"] == "ColumnTransformer + OneHotEncoder"
    assert data["Pipeline"] == "Loaded"
    assert data["Status"] == "Ready for Prediction"


def test_predict():

    sample_data = {
        "OverallQual": 7,
        "GrLivArea": 1710,
        "TotalBsmtSF": 856,
        "SecondFlrSF": 854,
        "BsmtFinSF1": 706,
        "FirstFlrSF": 856,
        "LotArea": 8450,
        "GarageArea": 548
    }

    response = client.post(
        "/predict",
        json=sample_data
    )

    assert response.status_code == 200

    prediction = response.json()

    assert "predicted_price" in prediction

    assert isinstance(prediction["predicted_price"], float)


def test_predict_invalid_data():

    sample_data = {
        "OverallQual": 7
    }

    response = client.post(
        "/predict",
        json=sample_data
    )

    assert response.status_code == 422