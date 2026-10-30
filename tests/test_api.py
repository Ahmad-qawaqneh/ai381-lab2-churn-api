
import json
from pathlib import Path

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict():
    project_root = Path(__file__).resolve().parents[1]

    with open(project_root / "sample_request.json") as f:
        sample = json.load(f)

    response = client.post("/predict", json=sample)

    assert response.status_code == 200

    result = response.json()
    assert "churn_probability" in result

    probability = result["churn_probability"]
    assert 0 <= probability <= 1
