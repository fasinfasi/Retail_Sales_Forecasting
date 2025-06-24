import pickle
import pandas as pd

try:
    with open("./models/model_best.pkl", "rb") as f:
        model = pickle.load(f)
except Exception as e:
    raise RuntimeError(f"Error loading model: {e}")


def predict(input_data: pd.DataFrame):
    print("input_data.columns:", input_data.columns.tolist())
    return model.predict(input_data)
