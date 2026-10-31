
import json
from pathlib import Path

from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def sample_customer():
    with open(PROJECT_ROOT / "sample_request.json") as f:
        return json.load(f)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict():
    response = client.post("/predict", json=sample_customer())
    assert response.status_code == 200
    assert "churn_probability" in response.json()


def test_probability_range():
    response = client.post("/predict", json=sample_customer())
    probability = response.json()["churn_probability"]
    assert 0 <= probability <= 1


def test_missing_required_field():
    customer = sample_customer()
    del customer["tenure_months"]

    response = client.post("/predict", json=customer)
    assert response.status_code == 422


def test_negative_tenure():
    customer = sample_customer()
    customer["tenure_months"] = -5

    response = client.post("/predict", json=customer)
    assert response.status_code == 422


def test_negative_monthly_charges():
    customer = sample_customer()
    customer["monthly_charges"] = -100

    response = client.post("/predict", json=customer)
    assert response.status_code == 422


def test_invalid_support_calls():
    customer = sample_customer()
    customer["support_calls"] = "invalid"

    response = client.post("/predict", json=customer)
    assert response.status_code == 422
