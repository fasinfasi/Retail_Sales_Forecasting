from fastapi import FastAPI
from .schema import SalesInput
from .model_loader import predict
import pandas as pd

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Retail Sales Forecast API!"}

@app.post("/predict")
def get_prediction(payload: SalesInput):
    try:
        input_df = pd.DataFrame([payload.dict()])
        print("Received input:\n", input_df)
        result = predict(input_df)
        print("Prediction result:", result)
        return {"prediction": result[0]}
    except Exception as e:
        print("Prediction failed:", e)
        return {"error": str(e)}

