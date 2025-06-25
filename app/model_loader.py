import pickle
import numpy as np
import pandas as pd

# Load the model
try:
    with open("./models/model_best.pkl", "rb") as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully.")
except Exception as e:
    print("❌ Error loading model:", e)

# Define prediction function compatible with FastAPI
def predict(data: pd.DataFrame):
    try:
        print("📦 Data received for prediction:", data)
        prediction = model.predict(data)
        print("✅ Prediction successful:", prediction)
        return prediction
    except Exception as e:
        print("❌ Prediction failed:", e)
        raise e
