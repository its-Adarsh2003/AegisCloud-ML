import streamlit as st
import boto3
import pandas as pd
import plotly.express as px
import io
import joblib
from datetime import datetime, timedelta


# ===== 1. CONFIG (sirf ye 3 cheeze apni dalni hain) =====
INSTANCE_ID = "i-052bbcbccf7277a40"          # yahan apna EC2 instance ID
REGION = "us-east-1"                         # tumhara region
BUCKET = "aegiscloud-ml-models-adarsh"       # tumhara S3 bucket
MODEL_KEY = "models/model.pkl"               # tumhara model path


# ===== 1.1 ANOMALY LOGIC THRESHOLDS =====
CPU_ALERT_THRESHOLD = 40.0      # percentage se upar ho to high CPU
SCORE_ALERT_THRESHOLD = 0.0     # score is lower = more anomalous (0 se niche ko suspicious maan rahe)


# ===== 2. PAGE SETTINGS =====
st.set_page_config(
    page_title="AegisCloud – EC2 Anomaly Monitor",
    page_icon="🛡️",
    layout="wide"
)
st.title("🛡️ AegisCloud – My EC2 Anomaly Monitor")


# ===== 3. HELPERS: AWS clients =====
def get_cloudwatch_client():
    return boto3.client("cloudwatch", region_name=REGION)


def get_s3_client():
    return boto3.client("s3", region_name=REGION)


# ===== 4. MODEL LOAD (S3 se) =====
@st.cache_resource
def load_model_from_s3():
    s3 = get_s3_client()
    obj = s3.get_object(Bucket=BUCKET, Key=MODEL_KEY)
    model = joblib.load(io.BytesIO(obj["Body"].read()))
    return model


# ===== 5. CPU DATA FETCH (CloudWatch se) =====
@st.cache_data(ttl=60)
def fetch_cpu_data_last_n_minutes(n_minutes: int = 60) -> pd.DataFrame:
    cw = get_cloudwatch_client()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=n_minutes)

    resp = cw.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName="CPUUtilization",
        Dimensions=[{"Name": "InstanceId", "Value": INSTANCE_ID}],
        StartTime=start_time,
        EndTime=end_time,
        Period=60,
        Statistics=["Average"],
    )  # [web:129]

    if not resp["Datapoints"]:
        return pd.DataFrame()

    df = pd.DataFrame(resp["Datapoints"])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df = df.sort_values("Timestamp")
    df = df.rename(columns={"Average": "cpu_value"})
    return df[["Timestamp", "cpu_value"]]


# ===== 6. FEATURE ENGINEERING (same as training) =====
def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["cpu_avg"] = df["cpu_value"].rolling(window=3, min_periods=1).mean()
    df["cpu_max"] = df["cpu_value"].rolling(window=3, min_periods=1).max()
    return df


# ===== 7. MAIN APP LOGIC =====
with st.spinner("Loading model from S3..."):
    model = load_model_from_s3()

with st.spinner("Fetching CPU metrics from CloudWatch..."):
    raw_df = fetch_cpu_data_last_n_minutes(60)

if raw_df.empty:
    st.error("No CPU data found in last 60 minutes")
    st.stop()

# Features add karo
df = add_features(raw_df)

# Model input
X = df[["cpu_avg", "cpu_max"]].fillna(0).values

# Prediction
preds = model.predict(X)               # 1 = normal, -1 = anomaly
scores = model.decision_function(X)    # lower = more anomalous [web:130][web:131]

df["prediction"] = preds
df["score"] = scores

latest = df.iloc[-1]


# ===== 8. LAYOUT – graph + metrics =====
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 CPU Utilization (last 60 min)")
    fig = px.line(
        df,
        x="Timestamp",
        y="cpu_value",
        title="CPU % over time",
        labels={"cpu_value": "CPU %"},
    )
    # anomalies ko red marker se highlight karo
    anomaly_points = df[df["prediction"] == -1]
    if not anomaly_points.empty:
        fig.add_scatter(
            x=anomaly_points["Timestamp"],
            y=anomaly_points["cpu_value"],
            mode="markers",
            marker=dict(color="red", size=8),
            name="Anomaly"
        )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📟 Current status")

    current_cpu = float(latest["cpu_value"])
    current_score = float(latest["score"])
    current_pred = int(latest["prediction"])

    st.metric("Current CPU", f"{current_cpu:.1f} %")
    st.metric("Latest anomaly score", f"{current_score:.3f}")

    # ===== HYBRID RULE + ML LOGIC =====
    is_score_anomalous = current_score < SCORE_ALERT_THRESHOLD
    is_cpu_high = current_cpu > CPU_ALERT_THRESHOLD

    # Optionally, agar tum chaho to model prediction bhi include kar sakte ho:
    # is_model_says_anomaly = (current_pred == -1)

    if is_score_anomalous and is_cpu_high:
        st.error("🚨 ML says: ANOMALY")
    else:
        st.success("✅ ML says: NORMAL")

    st.caption(
        "Note: Isolation Forest – lower score = more anomalous. "
        "[1 = normal, -1 = anomaly] – Status here also considers current CPU level."
    )


# ===== 9. TABLE VIEW (optional debug) =====
with st.expander("Raw data + predictions"):
    st.dataframe(
        df[["Timestamp", "cpu_value", "cpu_avg", "cpu_max", "prediction", "score"]].tail(20),
        use_container_width=True
    )
