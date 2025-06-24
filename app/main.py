from fastapi import FastAPI
from .schema import SalesInput
from .model_loader import predict
import pandas as pd

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Retail Sales Forecast API!"}

@app.post("/predict")
def get_prediction(data: SalesInput):
    try:
        df = pd.DataFrame([data.dict()])
        print("Incoming request data:", df)
        prediction = predict(df)
        return {"prediction": float(prediction[0])}
    except Exception as e:
        print("Prediction failed at API level:", e)
        return {"error": str(e)}
