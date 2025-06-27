import requests
import json

# Test data
test_payload = {
    "price": 10.5,
    "stock_available": 100,
    "day": 15,
    "month": 6,
    "year": 2025,
    "product_category": "Dairy",
    "store_location": "New York"
}

print("Testing API endpoint...")
print("Payload:", json.dumps(test_payload, indent=2))

try:
    # Test the API
    response = requests.post(
        "http://localhost:8001/predict",
        headers={"Content-Type": "application/json"},
        json=test_payload
    )
    
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Success! Prediction: {result}")
    else:
        print(f"Error Response: {response.text}")
        
        # Try to parse as JSON if possible
        try:
            error_details = response.json()
            print(f"Error Details: {json.dumps(error_details, indent=2)}")
        except:
            pass
            
except requests.exceptions.ConnectionError:
    print("❌ Connection Error: Make sure your FastAPI server is running on localhost:8001")
except Exception as e:
    print(f"❌ Unexpected Error: {e}")

print("\n" + "="*50)
print("If you see errors above, check:")
print("1. Is your FastAPI server running? (uvicorn main:app --reload --port 8001)")
print("2. Are there any error messages in the FastAPI console?")
print("3. Does your model file exist at ./models/model_best.pkl?")