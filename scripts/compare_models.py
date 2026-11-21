
"""Compare HomeValue AI Random Forest configurations."""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import KFold, cross_validate, train_test_split


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


def evaluate(name, model, x_train, y_train, cv):
    """Evaluate a model using five-fold cross-validation."""

    results = cross_validate(
        model,
        x_train,
        y_train,
        cv=cv,
        scoring={
            "r2": "r2",
            "mae": "neg_mean_absolute_error",
            "rmse": "neg_root_mean_squared_error",
        },
        n_jobs=1,
    )

    r2 = results["test_r2"]
    mae = -results["test_mae"]
    rmse = -results["test_rmse"]

    print(f"\n{name}")
    print("-" * 45)
    print(f"Average R2:   {r2.mean():.4f}")
    print(f"R2 Std Dev:   {r2.std():.4f}")
    print(f"Average MAE:  ${mae.mean():,.2f}")
    print(f"Average RMSE: ${rmse.mean():,.2f}")


def main():
    """Compare the production model against one candidate."""

    df = pd.read_csv(DATA_PATH)

    x = df[FEATURES]
    y = df["SalePrice"]

    # Use only the original development/training partition.
    x_train, _, y_train, _ = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
    )

    # Load the current production model as our baseline.
    saved_pipeline = joblib.load(MODEL_PATH)

    baseline = clone(saved_pipeline)

    # Test one candidate configuration.
    candidate = clone(saved_pipeline)
    candidate.set_params(
        model__n_estimators=200,
        model__min_samples_leaf=2,
        model__max_features=0.8,
        model__random_state=42,
        model__n_jobs=-1,
    )

    cv = KFold(
        n_splits=5,
        shuffle=True,
        random_state=42,
    )

    print("HomeValue AI - Model Comparison")
    print("=" * 45)
    print(f"Training samples: {len(x_train)}")
    print(f"Features: {len(FEATURES)}")
    print("Cross-validation folds: 5")

    evaluate("Current Random Forest", baseline, x_train, y_train, cv)
    evaluate("Candidate Random Forest", candidate, x_train, y_train, cv)

    print("\nProduction model remains unchanged.")


if __name__ == "__main__":
    main()
