
"""Tests for the HomeValue AI prediction module."""

import math

from src.predict import predict_house_price


SAMPLE_HOUSE = {
    "OverallQual": 7,
    "GrLivArea": 1710,
    "TotalBsmtSF": 856,
    "2ndFlrSF": 854,
    "BsmtFinSF1": 706,
    "1stFlrSF": 856,
    "LotArea": 8450,
    "GarageArea": 548,
}


def test_prediction_returns_valid_price():
    """The production model should return a positive, finite price."""
    prediction = predict_house_price(SAMPLE_HOUSE)

    assert isinstance(prediction, float)
    assert math.isfinite(prediction)
    assert prediction > 0


def test_prediction_is_deterministic():
    """Identical house details should produce identical predictions."""
    first_prediction = predict_house_price(SAMPLE_HOUSE)
    second_prediction = predict_house_price(SAMPLE_HOUSE)

    assert first_prediction == second_prediction


def test_prediction_does_not_modify_input():
    """Making a prediction should not change the supplied house data."""
    house_data = SAMPLE_HOUSE.copy()
    original_data = house_data.copy()

    predict_house_price(house_data)

    assert house_data == original_data
