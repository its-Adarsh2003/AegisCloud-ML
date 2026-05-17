AegisCloud-ML ☁️🤖

ML-powered cloud monitoring system for detecting EC2 CPU anomalies using AWS CloudWatch and Isolation Forest.

📌 Overview

AegisCloud-ML is a lightweight cloud monitoring and anomaly detection system built using AWS services and Machine Learning.

The project monitors AWS EC2 CPU utilization metrics from CloudWatch, applies an Isolation Forest anomaly detection model, and visualizes suspicious CPU behavior through an interactive Streamlit dashboard.

This project demonstrates:

Cloud Monitoring
AWS Integration
ML-based Anomaly Detection
Real-time Visualization
Automation Workflows
🚀 Features
📊 Real-time EC2 CPU monitoring using AWS CloudWatch
🤖 ML-based anomaly detection using Isolation Forest
☁️ AWS integration with EC2, S3, CloudWatch, and IAM
📈 Interactive Streamlit dashboard for visualization
🔄 Automated model loading from Amazon S3
⚡ Real-time anomaly scoring and alert visualization
🧪 Local Lambda-style testing environment
🛠️ Tech Stack
Cloud & DevOps
AWS EC2
AWS CloudWatch
AWS S3
AWS IAM
Programming & ML
Python
Scikit-learn
Pandas
NumPy
Boto3
Dashboard & Visualization
Streamlit
Plotly
🧠 Architecture
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
📂 Project Structure
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
⚙️ Installation

Clone the repository:

git clone https://github.com/its-Adarsh2003/AegisCloud-ML.git
cd AegisCloud-ML

Create virtual environment:

python -m venv .venv

Activate environment:

Windows
.venv\Scripts\activate
Linux/Mac
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt
▶️ Run the Project
Train the ML Model
python scripts/train_model.py
Run Local Testing
python scripts/local_lambda_test.py
Start Streamlit Dashboard
streamlit run dashboard.py
☁️ AWS Configuration

Ensure AWS credentials are configured:

aws configure

Required permissions:

cloudwatch:GetMetricStatistics
s3:GetObject
📊 ML Workflow

The system:

Fetches EC2 CPU metrics from CloudWatch
Builds rolling statistical features
Applies Isolation Forest anomaly detection
Scores anomalies in real time
Displays results on Streamlit dashboard
🔍 Example Use Cases
Cloud infrastructure monitoring
DevOps observability systems
AWS anomaly detection
CPU spike detection
MLOps monitoring workflows
Intelligent cloud dashboards
📸 Dashboard Preview

Add Streamlit dashboard screenshots here

Example:

/assets/dashboard.png
📈 Future Improvements
Docker containerization
Kubernetes deployment
CI/CD pipeline integration
Email/SNS anomaly alerts
Terraform infrastructure setup
Multi-instance monitoring
Grafana integration
🏆 Learning Outcomes

Through this project, I gained hands-on experience in:

AWS Cloud Monitoring
CloudWatch metric analysis
Machine Learning anomaly detection
Streamlit dashboard development
Cloud-native automation workflows
Real-time monitoring systems
👨‍💻 Author
Adarsh Dubey
GitHub: its-Adarsh2003
LinkedIn: Adarsh Dubey LinkedIn
⭐ If you found this project useful, consider giving it a star!
