
"""Evaluate the saved HomeValue AI prediction model."""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "train.csv"
MODEL_PATH = BASE_DIR / "models" / "house_price_pipeline_top8.pkl"

FEATURES = [
    "OverallQual",
    "GrLivArea",
    "TotalBsmtSF",
    "2ndFlrSF",
    "BsmtFinSF1",
    "1stFlrSF",
    "LotArea",
    "GarageArea",
]


def main():
    """Evaluate the existing production model."""

    print("\nHomeValue AI - Model Evaluation")
    print("-" * 40)

    # Load the original housing dataset.
    df = pd.read_csv(DATA_PATH)

    required_columns = FEATURES + ["SalePrice"]
    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing dataset columns: {missing_columns}"
        )

    X = df[FEATURES]
    y = df["SalePrice"]

    # Reproduce the original evaluation split.
    _, X_test, _, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    # Load the existing trained production pipeline.
    model = joblib.load(MODEL_PATH)

    # Generate predictions without retraining.
    predictions = model.predict(X_test)

    # Calculate regression metrics.
    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(
        y_test, predictions
    ) ** 0.5

    print(f"Dataset samples: {len(df)}")
    print(f"Evaluation samples: {len(X_test)}")
    print(f"Features used: {len(FEATURES)}")

    print("\nModel Performance")
    print("-" * 40)
    print(f"R2 Score: {r2:.6f}")
    print(f"MAE: ${mae:,.2f}")
    print(f"RMSE: ${rmse:,.2f}")

    print("\nEvaluation note:")
    print(
        "This reproduces the original development split. "
        "It is not an independent final evaluation."
    )


if __name__ == "__main__":
    main()
