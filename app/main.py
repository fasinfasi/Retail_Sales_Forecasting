from fastapi import FastAPI, HTTPException, Request
from schema import SalesInput
from model_loader import predict
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")
    
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Retail Sales Forecast API!"}

@app.get("/predict")
def predict_info():
    return {
        "message": "This is the prediction endpoint. Send a POST request with sales data.",
        "method": "POST",
        "required_fields": {
            "price": "float",
            "stock_available": "int", 
            "day": "int",
            "month": "int",
            "year": "int",
            "product_category": "string (Beverage, Dairy, Frozen, Household, Snack)",
            "store_location": "string (Los Angeles, New York, Chicago)"
        },
        "example": {
            "price": 12.99,
            "stock_available": 50,
            "day": 15,
            "month": 6,
            "year": 2025,
            "product_category": "Dairy",
            "store_location": "Los Angeles"
        }
    }

@app.post("/predict")
def get_prediction(data: SalesInput):
    try:
        raw = data.dict()
        print("Raw input data:", raw)
        
        df = pd.DataFrame([raw])
        print("DataFrame created:", df)
        
        prediction = predict(df)
        return {"prediction": float(prediction[0])}
        
    except Exception as e:
        print("Prediction failed at API level:", str(e))
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# ✅ Entry point for local or direct execution
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
