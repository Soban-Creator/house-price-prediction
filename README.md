
# HomeValue AI
### Intelligent House Price Prediction System

An end-to-end machine learning application that estimates residential property prices through a Streamlit web interface and a FastAPI prediction service.

**Built with Python, Scikit-learn, Random Forest, FastAPI, Streamlit, and Docker.**

---

## Project Overview

HomeValue AI demonstrates the complete workflow of developing and integrating a machine learning model into a web application.

Users enter eight property characteristics through the frontend. The application sends those values to a FastAPI backend, which validates the inputs and uses a trained Random Forest regression pipeline to generate an estimated selling price.

The project includes:

- Exploratory data analysis and model development
- Feature selection and preprocessing
- A serialized machine learning pipeline
- REST API development and input validation
- A custom Streamlit user interface
- Automated API testing
- Docker containerization
- Reproducible model evaluation and comparison

## Key Features

- **Property price estimation:** Predict prices using eight numerical property features.
- **Interactive frontend:** A custom Streamlit interface with a Warm Sage visual design.
- **Machine learning API:** FastAPI endpoints for predictions, health checks, and model information.
- **Input validation:** Pydantic checks required values, numeric constraints, and invalid numbers.
- **Error handling:** The backend handles prediction failures without exposing internal error details to API clients.
- **Model evaluation:** Scripts reproduce evaluation metrics and compare candidate model configurations.
- **Automated testing:** A suite of 25 API tests.
- **Docker support:** Containerized FastAPI backend for reproducible deployment.

## System Architecture

```text
             HomeValue AI
                   |
          Streamlit Frontend
             frontend/app.py
                   |
             HTTP Request
                   |
             FastAPI Backend
               api/main.py
                   |
          Pydantic Validation
                   |
           Prediction Module
             src/predict.py
                   |
       Saved Scikit-learn Pipeline
                   |
             ColumnTransformer
         (8 numerical features)
                   |
          RandomForestRegressor
                   |
          Predicted House Price
                   |
         FastAPI JSON Response
                   |
          Streamlit Frontend
```

The frontend does not execute the machine learning model directly. It communicates with the FastAPI backend, which loads the saved pipeline and performs prediction.

## Dataset

**Source:** [House Prices - Advanced Regression Techniques](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques)

The project uses the Ames housing dataset provided through Kaggle.

| Property | Details |
|---|---|
| Training records | 1,460 houses |
| Prediction target | `SalePrice` |
| Final model inputs | 8 numerical features |
| Price currency | USD |
| Problem type | Supervised regression |

The underlying dataset contains additional numerical and categorical variables, but the production model uses only the eight features listed below.

## Production Model Features

| API input | Model feature | Description |
|---|---|---|
| `OverallQual` | `OverallQual` | Overall material and finish quality, from 1 to 10 |
| `GrLivArea` | `GrLivArea` | Above-ground living area in square feet |
| `TotalBsmtSF` | `TotalBsmtSF` | Total basement area |
| `SecondFlrSF` | `2ndFlrSF` | Second-floor area |
| `BsmtFinSF1` | `BsmtFinSF1` | Type 1 finished basement area |
| `FirstFlrSF` | `1stFlrSF` | First-floor area |
| `LotArea` | `LotArea` | Total lot area |
| `GarageArea` | `GarageArea` | Garage area |

The API uses readable Python field names for the first-floor and second-floor inputs and converts them to the names expected by the saved model.

## Machine Learning Model

**Algorithm:** Random Forest Regressor

**Production model file:**

`models/house_price_pipeline_top8.pkl`

The serialized Scikit-learn pipeline contains:

1. `ColumnTransformer` for preprocessing.
2. Eight numerical features configured with passthrough transformation.
3. `RandomForestRegressor` for price prediction.

The saved transformer also contains a configured `OneHotEncoder` branch, but that branch has no assigned categorical features in the production model. Therefore, no categorical encoding is performed during prediction.

The pipeline is loaded using Joblib.

### Model Performance

The production model was evaluated using the project's recorded 80/20 training and testing split procedure with `random_state=42`.

| Metric | Result |
|---|---:|
| R² Score | 0.8897 |
| Mean Absolute Error (MAE) | $19,113.32 |
| Root Mean Squared Error (RMSE) | $29,085.46 |

**Metric interpretation:**

- **R²:** Measures how much variation in the target is explained by the model on the evaluated data.
- **MAE:** Measures the average absolute difference between predicted and actual prices.
- **RMSE:** Measures prediction error while placing greater weight on larger errors.

These results were reproduced using the project's existing dataset and split procedure. They should not be interpreted as validation on a new, independent external dataset.

### Model Comparison

The repository includes a script for comparing the existing Random Forest pipeline against an alternative configuration using five-fold cross-validation.

The alternative showed only a small improvement in average cross-validation metrics, so the existing production model was retained.

No replacement model was deployed as part of the optimization process.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming language | Python |
| Data processing | Pandas, NumPy |
| Machine learning | Scikit-learn, Random Forest |
| Model serialization | Joblib |
| Backend | FastAPI, Pydantic, Uvicorn |
| Frontend | Streamlit |
| Testing | Pytest |
| Containerization | Docker |
| Version control | Git and GitHub |

## Project Structure

```text
house-price-prediction/
|
|-- api/
|   `-- main.py
|
|-- app/
|-- config/
|-- data/
|
|-- frontend/
|   `-- app.py
|
|-- models/
|   `-- house_price_pipeline_top8.pkl
|
|-- notebooks/
|   `-- 01_eda.ipynb
|
|-- scripts/
|   |-- evaluate_model.py
|   `-- compare_models.py
|
|-- src/
|   `-- predict.py
|
|-- tests/
|   `-- test_api.py
|
|-- .dockerignore
|-- .gitignore
|-- Dockerfile
|-- requirements.txt
|-- requirements-dev.txt
`-- README.md
```

The structure above highlights the main application components. The repository also retains earlier development artifacts and model experiments.

## Installation

### Prerequisites

- Python 3.12 recommended
- Git
- A supported terminal
- Docker Desktop, if using Docker

### 1. Clone the repository

```bash
git clone https://github.com/Soban-Creator/house-price-prediction.git
cd house-price-prediction
```

### 2. Create a virtual environment

On Windows Command Prompt:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Running the Application Locally

The FastAPI backend and Streamlit frontend must run at the same time.

### 1. Start the FastAPI backend

From the repository root:

```bash
python -m uvicorn api.main:app --reload
```

The backend runs at:

`http://127.0.0.1:8000`

Useful endpoints:

- API documentation: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`
- Model information: `http://127.0.0.1:8000/model-info`

### 2. Start the Streamlit frontend

Open a second terminal, activate the same virtual environment, and run:

```bash
python -m streamlit run frontend/app.py
```

Streamlit typically opens at:

`http://localhost:8501`

Enter the property details and use the interface to request an estimated price.

## REST API Reference

### GET `/`

Returns the application's welcome message.

### GET `/health`

Returns the API's health response.

Example:

```json
{
  "status": "Healthy"
}
```

### GET `/model-info`

Returns information about the configured production model and preprocessing pipeline.

### POST `/predict`

Accepts eight required property inputs and returns an estimated house price.

**Example request:**

```json
{
  "OverallQual": 7,
  "GrLivArea": 1710,
  "TotalBsmtSF": 856,
  "SecondFlrSF": 854,
  "BsmtFinSF1": 706,
  "FirstFlrSF": 856,
  "LotArea": 8450,
  "GarageArea": 548
}
```

**Response format:**

```json
{
  "predicted_price": 206521.0
}
```

The number above illustrates the JSON response structure only. Actual predictions depend on the input values and trained model.

Request validation errors return HTTP 422. Unexpected prediction failures return HTTP 500 with a generic error message.

For interactive API testing, visit:

`http://127.0.0.1:8000/docs`

## Docker Setup

The repository includes a Dockerfile for the FastAPI backend.

### 1. Build the image

Run from the repository root:

```bash
docker build -t homevalue-ai-api:local .
```

### 2. Start the container

```bash
docker run --rm -p 8000:8000 homevalue-ai-api:local
```

The backend will be available at:

`http://127.0.0.1:8000`

### 3. Run the frontend separately

With the Docker backend running, start the Streamlit frontend from your local Python environment:

```bash
python -m streamlit run frontend/app.py
```

The Docker image currently packages the backend, prediction module, and model files. The Streamlit frontend runs separately.

### Alternative Docker Port

If local port 8000 is occupied:

```bash
docker run --rm -p 8001:8000 homevalue-ai-api:local
```

Then configure the frontend to use:

`HOUSE_PRICE_API_URL=http://127.0.0.1:8001`

For Windows Command Prompt:

```cmd
set HOUSE_PRICE_API_URL=http://127.0.0.1:8001
python -m streamlit run frontend/app.py
```

## Automated Testing

Install the application and testing dependencies:

```bash
python -m pip install -r requirements.txt -r requirements-dev.txt
```

Run the API test suite:

```bash
python -m pytest tests/test_api.py -q
```

**Most recently verified local result:**

```text
25 passed, 1 warning
```

The warning was produced by a deprecation notice in the installed API testing dependencies. It did not cause any tests to fail.

## Reproducible Model Evaluation

Run the production model evaluation:

```bash
python scripts/evaluate_model.py
```

Compare the production model with an alternative Random Forest configuration:

```bash
python scripts/compare_models.py
```

These scripts support reproducible analysis without replacing the production model artifact.

## Current Limitations

- The model was developed using the historical Ames housing dataset.
- Predictions are expressed in the dataset's USD price context.
- The model accepts only eight numerical features and does not account for every factor affecting real estate prices.
- Performance may differ substantially for properties outside the training data's market and time period.
- The reported evaluation is not an independent external-market validation.
- Predictions are estimates, not professional property appraisals or financial advice.

## Future Improvements

Potential future enhancements include:

- Public deployment of the frontend and backend
- Automated CI checks on GitHub
- Additional model interpretability and explainability
- Evaluation against newer, independent housing data
- Further model experimentation where measurable improvements justify replacement

## Author

**Syed Soban Mudassar**

BS Software Engineering

COMSATS University Islamabad, Wah Campus

GitHub: [Soban-Creator](https://github.com/Soban-Creator)

---

*Developed as an educational and internship machine learning project.*
