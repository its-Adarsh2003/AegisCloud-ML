# AegisCloud-ML

Lightweight ML toolkit to monitor EC2 CPU anomalies using an Isolation Forest.

## Overview

This repo trains an unsupervised anomaly detector (Isolation Forest) on EC2 CPUUtilization metrics, saves the model, and provides:
- a training script (`scripts/train_model.py`)
- a local test / lambda shim (`scripts/local_lambda_test.py`)
- a Streamlit dashboard (`dashboard.py`) that fetches live CloudWatch metrics and scores them with the model
- a small utility to verify loading the model from S3 (`test_load_model.py`)

The model is persisted as `models/model.pkl` and can be uploaded to S3 for the dashboard to load.

## Repository layout

- `dashboard.py` — Streamlit app that loads a model from S3, fetches CloudWatch CPU metrics, builds features, predicts anomalies, and shows visualizations.
- `test_load_model.py` — simple script to load the model directly from S3 using `boto3` (useful to verify AWS connectivity).
- `scripts/train_model.py` — trains an `IsolationForest` on `data/cpu_real.csv` and writes `models/model.pkl`.
- `scripts/local_lambda_test.py` — small local runner which loads `models/model.pkl` and runs sample predictions (useful for CI or lambda emulation).
- `data/cpu_real.csv` — sample CloudWatch-exported CSV used by the trainer.
- `models/model.pkl` — pre-trained model saved by `train_model.py`.

## Key concepts

- Feature engineering: the trainer computes rolling statistics over CPU samples (`cpu_avg`, `cpu_max`) to remove noise and give the Isolation Forest stable signals.
- Isolation Forest: unsupervised anomaly detector; model outputs `1` for normal and `-1` for anomaly. The `decision_function` gives a score where lower values are more anomalous.
- Hybrid rule: dashboard combines ML score with a CPU threshold to avoid false positives (e.g., high CPU + anomalous ML score → alert).

## Prerequisites

- Python 3.9+ (tested on 3.10)
- A virtual environment (recommended)
- AWS CLI configured or AWS environment variables set, with permissions for:
  - `s3:GetObject` (for model load)
  - `cloudwatch:GetMetricStatistics` (for dashboard metric reads)

## Recommended install

Create + activate virtualenv (Windows example):

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -U pip
pip install boto3 pandas scikit-learn joblib streamlit plotly
```

Optional: create a `requirements.txt` with the above packages for reproducible installs.

## Quickstart — train locally

1. Verify your `data/cpu_real.csv` is present and looks like CloudWatch CSV (timestamp, value rows).
2. Run the trainer to build features, train the model, and save `models/model.pkl`:

```bash
python scripts/train_model.py
```

This writes `models/model.pkl` which `scripts/local_lambda_test.py` and the dashboard can load.

## Quickstart — test local predictions

Run the simple test harness to validate the saved model behaves as expected:

```bash
python scripts/local_lambda_test.py
```

It will print predictions/scores for a normal and an anomalous sample.

## Dashboard (Streamlit)

1. Set configuration variables at the top of `dashboard.py`: `INSTANCE_ID`, `REGION`, `BUCKET`, `MODEL_KEY`.
2. Ensure AWS credentials are available to `boto3` (e.g., `aws configure` or environment variables).
3. Run Streamlit:

```bash
streamlit run dashboard.py
```

Streamlit will open in your browser. The app caches the model and CloudWatch data for a short TTL for interactive speed.

## Using S3 for the model

- If you want the dashboard to use the cloud-hosted model, upload `models/model.pkl` to your S3 bucket at `models/model.pkl` (or update `MODEL_KEY`).
- Ensure the IAM role or user used by `boto3` has `s3:GetObject` for that key.

Example (AWS CLI):

```bash
aws s3 cp models/model.pkl s3://<your-bucket>/models/model.pkl
```

## Troubleshooting

- No CloudWatch datapoints: check `INSTANCE_ID`, `REGION`, and that the instance is emitting `CPUUtilization` metrics.
- boto3 permission errors: confirm IAM policy and that credentials are valid.
- Model load fails locally: ensure `models/model.pkl` exists and was written by the same scikit-learn version, or retrain locally with `train_model.py`.

## Recommended next steps

- Add `requirements.txt` and CI job to run `scripts/local_lambda_test.py` on each push.
- Add unit tests for `load_data()` and `build_features()` to lock expected behavior.
- Add an upload helper script to push `models/model.pkl` to S3 automatically after training.
- Add more robust error handling and logging around network calls.

## Contact / License

This is a learning/demo project. Use freely for experimentation. If you want, I can add a `LICENSE` file or prepare a `requirements.txt` and CI pipeline next.
