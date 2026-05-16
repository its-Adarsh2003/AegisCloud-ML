import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
from pathlib import Path
import warnings

# Suppress sklearn warnings for cleaner output
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')


def load_data(csv_path: str) -> pd.DataFrame:
    """
    CloudWatch CSV format:
    Id,m2
    StatusCode,Complete
    Messages,
    Full label,us-east-1:AWS/EC2 InstanceId:... CPUUtilization Average 300
    Label,CPUUtilization
    2026/02/14 14:20:00,2.13
    2026/02/14 14:25:00,2.10
    ...
    """
    df_raw = pd.read_csv(
        csv_path,
        header=None,
        names=["col1", "col2"],
        skipinitialspace=True
    )

    def is_timestamp(val):
        try:
            pd.to_datetime(val, format="%Y/%m/%d %H:%M:%S")
            return True
        except Exception:
            return False

    mask = df_raw["col1"].apply(is_timestamp)
    df = df_raw[mask].copy()

    df.rename(columns={"col1": "timestamp", "col2": "cpu_value"}, inplace=True)

    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y/%m/%d %H:%M:%S")
    df["cpu_value"] = pd.to_numeric(df["cpu_value"])

    df = df.sort_values("timestamp")
    return df


def build_features(df: pd.DataFrame, window_size: int = 5) -> pd.DataFrame:
    df = df.copy()
    df["cpu_avg"] = df["cpu_value"].rolling(window=window_size, min_periods=1).mean()
    df["cpu_max"] = df["cpu_value"].rolling(window=window_size, min_periods=1).max()
    features = df[["cpu_avg", "cpu_max"]].dropna()
    return features


def train_isolation_forest(X: pd.DataFrame) -> IsolationForest:
    model = IsolationForest(
        n_estimators=100,
        contamination=0.15,
        random_state=42
    )
    model.fit(X)
    return model


def main():
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "data" / "cpu_real.csv"   # yahan tumhari CPUUtilization CSV rakho
    models_dir = base_dir / "models"
    models_dir.mkdir(exist_ok=True)

    print("\n" + "="*60)
    print("🚀 MODEL TRAINING STARTED")
    print("="*60)
    
    print(f"\n📂 Loading data from: {data_path}")
    df = load_data(str(data_path))
    print(f"✅ Data loaded: {len(df)} rows")
    print(f"   Timestamp range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"   CPU values: min={df['cpu_value'].min():.2f}, max={df['cpu_value'].max():.2f}")
    
    print(f"\n🔧 Building features (window_size=5)...")
    X = build_features(df, window_size=5)
    print(f"✅ Features built: {len(X)} samples")
    
    print(f"\n🤖 Training Isolation Forest model...")
    model = train_isolation_forest(X)
    print(f"✅ Model trained successfully")

    print(f"\n💾 Saving model...")
    model_path = models_dir / "model.pkl"
    joblib.dump(model, model_path)
    print(f"✅ Model saved to: {model_path}")
    
    print("\n" + "="*60)
    print("🎉 TRAINING COMPLETED SUCCESSFULLY")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
