import joblib
import statistics
from pathlib import Path
import warnings

# Suppress sklearn warnings for cleaner output
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

def load_model():
    base_dir = Path(__file__).resolve().parent.parent
    model_path = base_dir / "models" / "model.pkl"
    model = joblib.load(model_path)
    return model

def build_features_from_list(cpu_values):
    cpu_avg = statistics.mean(cpu_values)
    cpu_max = max(cpu_values)
    return [[cpu_avg, cpu_max]]

def predict_anomaly(model, cpu_values):
    X = build_features_from_list(cpu_values)
    scores = model.decision_function(X)   # higher = more normal [web:28]
    preds = model.predict(X)              # -1 = anomaly, 1 = normal [web:28]
    return preds[0], scores[0]

def main():
    print("\n" + "="*60)
    print("🧪 ANOMALY DETECTION TEST")
    print("="*60)
    
    print("\n📦 Loading model...")
    model = load_model()
    print("✅ Model loaded successfully")

    normal_sample = [20, 25, 30, 35, 28]
    anomaly_sample = [85, 90, 95, 92, 88]

    print("\n🔍 Testing samples:\n")
    for label, sample in [("NORMAL", normal_sample), ("ANOMALY", anomaly_sample)]:
        pred, score = predict_anomaly(model, sample)
        status = "✅ NORMAL" if pred == 1 else "⚠️  ANOMALY"
        print(f"   {status}")
        print(f"   Sample:     {sample}")
        print(f"   Prediction: {pred}")
        print(f"   Score:      {score:.4f}")
        print()
    
    print("="*60)
    print("✅ TEST COMPLETED")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
