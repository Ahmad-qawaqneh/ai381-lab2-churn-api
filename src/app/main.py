
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

# Find the model relative to this file, not the terminal location.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "model.joblib"

FEATURES = [
    "tenure_months",
    "monthly_charges",
    "contract",
    "internet_service",
    "support_calls",
]


class CustomerInput(BaseModel):
    tenure_months: int = Field(ge=0)
    monthly_charges: float = Field(ge=0)
    contract: str
    internet_service: str
    support_calls: int = Field(ge=0)


app = FastAPI(title="AI381 Lab 2 Churn API")

model = joblib.load(MODEL_PATH)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(customer: CustomerInput):
    customer_data = customer.model_dump()
    X = pd.DataFrame([customer_data])[FEATURES]

    probability = float(model.predict_proba(X)[0, 1])

    return {"churn_probability": round(probability, 3)}
