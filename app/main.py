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
    input_df = pd.DataFrame([payload.dict()])
    result = predict(input_df)
    return {"prediction": result[0]}
