import pickle
import pandas as pd

with open("./models/model_best.pkl", "rb") as f:
    model = pickle.load(f)

def predict(input_data: pd.DataFrame):
    prediction = model.predict(input_data)
    return prediction