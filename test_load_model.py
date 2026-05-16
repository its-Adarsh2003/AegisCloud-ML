import boto3
import io
import joblib

BUCKET = "aegiscloud-ml-models-adarsh"
MODEL_KEY = "models/model.pkl"

# AWS credentials/region tumhare machine pe aws configure se set hone chahiye
s3 = boto3.client("s3")

obj = s3.get_object(Bucket=BUCKET, Key=MODEL_KEY)  # S3 se object lao
model = joblib.load(io.BytesIO(obj["Body"].read()))  # Bytes ko model me load karo

print("✅ Model loaded from S3")
print("Model type:", type(model))
