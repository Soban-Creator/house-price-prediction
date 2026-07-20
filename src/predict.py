import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PIPELINE_PATH = BASE_DIR / "models" / "house_price_pipeline_top8.pkl"

pipeline = joblib.load(PIPELINE_PATH)


def predict_house_price(input_data: dict):

    input_df = pd.DataFrame([input_data])

    prediction = pipeline.predict(input_df)

    return float(prediction[0])