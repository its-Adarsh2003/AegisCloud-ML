# AegisCloud-ML ☁️🤖

ML-powered cloud monitoring system for detecting EC2 CPU anomalies using AWS CloudWatch and Isolation Forest.

---

## 📌 Overview

AegisCloud-ML is a lightweight cloud monitoring and anomaly detection system built using AWS services and Machine Learning.

The project monitors AWS EC2 CPU utilization metrics from CloudWatch, applies an Isolation Forest anomaly detection model, and visualizes suspicious CPU behavior through an interactive Streamlit dashboard.

### Key Highlights
- Real-time EC2 CPU monitoring
- ML-based anomaly detection
- AWS CloudWatch integration
- Interactive Streamlit dashboard
- Automated model loading from Amazon S3
- Cloud-native monitoring workflow

---

## 🚀 Features

- 📊 Monitor EC2 CPU utilization using AWS CloudWatch
- 🤖 Detect anomalies using Isolation Forest
- ☁️ Integrate AWS services including EC2, S3, CloudWatch, and IAM
- 📈 Visualize metrics and anomalies with Streamlit dashboards
- ⚡ Perform real-time anomaly scoring
- 🔄 Load trained models directly from Amazon S3
- 🧪 Run local Lambda-style testing workflows

---

## 🛠️ Tech Stack

### Cloud & DevOps
- AWS EC2
- AWS CloudWatch
- AWS S3
- AWS IAM

### Programming & ML
- Python
- Scikit-learn
- Pandas
- NumPy
- Boto3

### Dashboard & Visualization
- Streamlit
- Plotly

---

## 🧠 System Architecture

```text
EC2 Instance
      ↓
CloudWatch Metrics
      ↓
Feature Engineering Pipeline
      ↓
Isolation Forest Model
      ↓
Anomaly Detection Engine
      ↓
Streamlit Dashboard
```

---

## 📂 Project Structure

```bash
AegisCloud-ML/
│
├── dashboard.py
├── test_load_model.py
│
├── scripts/
│   ├── train_model.py
│   └── local_lambda_test.py
│
├── data/
│   └── cpu_real.csv
│
├── models/
│   └── model.pkl
│
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/its-Adarsh2003/AegisCloud-ML.git
cd AegisCloud-ML
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

### Windows
```bash
.venv\Scripts\activate
```

### Linux / macOS
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

### Train the ML Model

```bash
python scripts/train_model.py
```

### Run Local Testing

```bash
python scripts/local_lambda_test.py
```

### Launch the Streamlit Dashboard

```bash
streamlit run dashboard.py
```

---

## ☁️ AWS Configuration

Configure AWS credentials before running the application:

```bash
aws configure
```

### Required IAM Permissions
- `cloudwatch:GetMetricStatistics`
- `s3:GetObject`

---

## 📊 ML Workflow

The system performs the following steps:

1. Fetches EC2 CPU metrics from AWS CloudWatch
2. Builds rolling statistical features
3. Applies Isolation Forest anomaly detection
4. Scores anomalies in real time
5. Displays results on the Streamlit dashboard

---

## 🔍 Use Cases

- Cloud infrastructure monitoring
- DevOps observability systems
- AWS anomaly detection
- CPU spike detection
- MLOps monitoring workflows
- Intelligent cloud dashboards

---

## 📸 Dashboard Preview

Add dashboard screenshots here.

Example:

```text
/assets/dashboard.png
```

---

## 📈 Future Improvements

- Docker containerization
- Kubernetes deployment
- CI/CD pipeline integration
- SNS or email alerting
- Terraform infrastructure setup
- Multi-instance monitoring
- Grafana integration

---

## 🏆 Learning Outcomes

This project helped build hands-on experience in:

- AWS cloud monitoring
- CloudWatch metric analysis
- ML-based anomaly detection
- Streamlit dashboard development
- Cloud-native automation workflows
- Real-time monitoring systems

---

## 👨‍💻 Author

### Adarsh Dubey

- GitHub: https://github.com/its-Adarsh2003
- LinkedIn: https://www.linkedin.com/in/adarsh-dubey-81881a2a5

---

## ⭐ Support

If you found this project useful, consider giving it a star.
