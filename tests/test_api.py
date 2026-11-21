
"""Automated API tests for HomeValue AI."""

import math

import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


@pytest.fixture
def sample_house():
    """Return valid sample property information."""
    return {
        "OverallQual": 7,
        "GrLivArea": 1710,
        "TotalBsmtSF": 856,
        "SecondFlrSF": 854,
        "BsmtFinSF1": 706,
        "FirstFlrSF": 856,
        "LotArea": 8450,
        "GarageArea": 548,
    }


def test_home():
    """Verify the API welcome endpoint."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the House Price Prediction API!"
    }


def test_health():
    """Verify the API health endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "Healthy"


def test_model_info():
    """Verify model information is available."""
    response = client.get("/model-info")

    assert response.status_code == 200

    data = response.json()

    assert data["Model"] == "Random Forest Regressor"
    assert data["Pipeline"] == "Loaded"
    assert data["Status"] == "Ready for Prediction"


def test_predict_valid_house(sample_house):
    """Verify a valid request produces a positive price."""
    response = client.post(
        "/predict",
        json=sample_house,
    )

    assert response.status_code == 200

    data = response.json()

    assert "predicted_price" in data
    assert isinstance(data["predicted_price"], float)
    assert math.isfinite(data["predicted_price"])
    assert data["predicted_price"] > 0


def test_predict_missing_fields():
    """Verify incomplete requests are rejected."""
    response = client.post(
        "/predict",
        json={"OverallQual": 7},
    )

    assert response.status_code == 422


def test_predict_empty_request():
    """Verify an empty request is rejected."""
    response = client.post(
        "/predict",
        json={},
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    "invalid_quality",
    [0, -1, 11, 100],
)
def test_invalid_quality(sample_house, invalid_quality):
    """Verify quality values outside 1-10 are rejected."""
    sample_house["OverallQual"] = invalid_quality

    response = client.post(
        "/predict",
        json=sample_house,
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    "field_name",
    [
        "GrLivArea",
        "TotalBsmtSF",
        "SecondFlrSF",
        "BsmtFinSF1",
        "FirstFlrSF",
        "LotArea",
        "GarageArea",
    ],
)
def test_negative_property_areas(sample_house, field_name):
    """Verify negative property areas are rejected."""
    sample_house[field_name] = -100

    response = client.post(
        "/predict",
        json=sample_house,
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    "field_name",
    ["GrLivArea", "FirstFlrSF", "LotArea"],
)
def test_required_positive_areas(sample_house, field_name):
    """Verify required property areas cannot be zero."""
    sample_house[field_name] = 0

    response = client.post(
        "/predict",
        json=sample_house,
    )

    assert response.status_code == 422


def test_model_failure(sample_house, monkeypatch):
    """Verify unexpected model errors return HTTP 500."""

    def failing_prediction(_input_data):
        raise RuntimeError("Simulated model failure")

    monkeypatch.setattr(
        "api.main.predict_house_price",
        failing_prediction,
    )

    response = client.post(
        "/predict",
        json=sample_house,
    )

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "Unable to generate a house price prediction."
    )


@pytest.mark.parametrize(
    "invalid_prediction",
    [float("nan"), float("inf"), -100.0, 0.0],
)
def test_invalid_model_output(
    sample_house,
    monkeypatch,
    invalid_prediction,
):
    """Verify invalid model outputs are rejected."""

    def invalid_predictor(_input_data):
        return invalid_prediction

    monkeypatch.setattr(
        "api.main.predict_house_price",
        invalid_predictor,
    )

    response = client.post(
        "/predict",
        json=sample_house,
    )

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "Unable to generate a house price prediction."
    )
