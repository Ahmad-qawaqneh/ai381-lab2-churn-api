
# AI381 Lab 2 — Churn Prediction API

**Course:** AI381 Machine Learning Operations  
**University:** Jordan University of Science and Technology  
**Project:** Bring Your Own Model — Container + CI

[![AI381 Lab 2 CI](https://github.com/Ahmad-qawaqneh/ai381-lab2-churn-api/actions/workflows/ci.yml/badge.svg)](https://github.com/Ahmad-qawaqneh/ai381-lab2-churn-api/actions/workflows/ci.yml)

## Project Overview

This project deploys a machine learning model for customer churn prediction using FastAPI, Docker, and GitHub Actions.

The project includes:
- A refactored training pipeline
- A FastAPI prediction service
- Pydantic input validation
- Seven automated API tests
- Ruff code linting
- A multi-stage Docker image
- A non-root container user
- A Docker health check
- Trivy vulnerability scanning
- Automated publishing to GitHub Container Registry (GHCR)
- GitHub Actions pinned to full commit SHAs

## Project Structure

```text
churn-api/
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   ├── app/
│   │   └── main.py
│   └── train/
│       └── train.py
├── tests/
│   └── test_api.py
├── Dockerfile
├── requirements.txt
├── model.joblib
├── churn_v2.csv
└── README.md
```

## Quick Start — One Command

With Docker installed, run:

```bash
docker run --rm -p 8000:8000 ghcr.io/ahmad-qawaqneh/ai381-lab2-churn-api:latest
```

The API will be available at:

http://localhost:8000

If the published package is private, authenticate to GHCR before pulling the image.

## API Endpoints

### Health Check

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

### Predict Customer Churn

**Endpoint:** `POST /predict`

Example request:

```json
{
  "tenure_months": 12,
  "monthly_charges": 65.5,
  "contract": "Month-to-month",
  "internet_service": "Fiber optic",
  "support_calls": 2
}
```

Example using PowerShell:

```powershell
$body = @{
    tenure_months = 12
    monthly_charges = 65.5
    contract = "Month-to-month"
    internet_service = "Fiber optic"
    support_calls = 2
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/predict -Method Post -ContentType "application/json" -Body $body
```

The API returns a churn prediction and probability.

Invalid requests, such as negative tenure or missing required fields, are rejected with HTTP 422.

## Run Locally Without Docker

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the API:

```bash
python -m uvicorn src.app.main:app --host 0.0.0.0 --port 8000
```

## Retrain the Model

```bash
python -m src.train.train
```

The training script reads `churn_v2.csv` and saves a retrained model as `model_retrained.joblib`.

The deployed API uses the existing `model.joblib`.

## Automated Testing

Run Ruff:

```bash
python -m ruff check src tests
```

Run pytest:

```bash
python -m pytest -v
```

The project contains seven API tests covering successful requests, health checks, and input validation.

## Docker Security

The Dockerfile implements:

- Multi-stage builds
- Pinned Python base-image version
- Non-root execution using UID 10001
- Docker HEALTHCHECK
- Port 8000 exposure

Build locally:

```bash
docker build -t ai381-churn-api:local .
```

Run locally:

```bash
docker run --rm -p 8000:8000 ai381-churn-api:local
```

## CI/CD Pipeline

GitHub Actions runs automatically for pull requests into `main` and pushes to `main`.

The pipeline:

1. Checks out the repository
2. Sets up Python 3.11
3. Installs dependencies
4. Runs Ruff linting
5. Runs pytest
6. Builds the Docker image
7. Scans the image with Trivy
8. Publishes the image to GHCR on pushes to `main`

The workflow uses full commit SHA pins for third-party GitHub Actions.

Trivy reports HIGH and CRITICAL findings. Its current configuration reports vulnerabilities without automatically failing CI.

## Published Container Image

**Image:**

```text
ghcr.io/ahmad-qawaqneh/ai381-lab2-churn-api:latest
```

**Published SHA-256 digest:**

```text
sha256:8f024a73c927031065e4dea3d0208d9e59e616a3af66883190064b4b4378089c
```

To inspect the published image:

```bash
docker buildx imagetools inspect ghcr.io/ahmad-qawaqneh/ai381-lab2-churn-api:latest
```

## Repository and Pull Request

GitHub repository:

https://github.com/Ahmad-qawaqneh/ai381-lab2-churn-api

The Lab 2 changes were developed on the `lab2-rubric-updates` branch, checked by GitHub Actions, and merged into the protected `main` branch through a pull request.

## Submission Evidence

The demonstration includes:

- Training and API project structure
- Pydantic validation
- Seven passing pytest tests
- Ruff linting
- Multi-stage Dockerfile
- Non-root container and healthy Docker status
- Green GitHub Actions workflow
- Trivy scan
- Protected branch and merged pull request
- Published GHCR image and SHA-256 digest
