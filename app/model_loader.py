import pickle
import pandas as pd
from datetime import datetime

# Load the model
try:
    with open("./models/model_best.pkl", "rb") as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully.")
except Exception as e:
    print("❌ Error loading model:", e)
    model = None

def predict(data: pd.DataFrame):
    if model is None:
        raise Exception("Model not loaded properly")
    
    try:
        print("📦 Raw data received:", data)
        
        # Make a copy to avoid modifying original
        df = data.copy()
        
        # Calculate weekday from date
        df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
        df['weekday'] = df['date'].dt.day_name()
        
        # Calculate revenue (price * stock_available as a proxy)
        df['revenue'] = df['price'] * df['stock_available']
        
        # One-hot encode categorical variables
        
        # Store ID encoding (based on your model's expected features)
        store_ids = ['str_02', 'str_03']  # Adjust based on your training data
        for store_id in store_ids:
            df[f'store_id_{store_id}'] = 0.0  # Default to 0, adjust logic if needed
        
        # Product ID encoding (based on your model's expected features) 
        product_ids = ['pdt_002', 'pdt_003', 'pdt_004', 'pdt_005']
        for product_id in product_ids:
            df[f'product_id_{product_id}'] = 0.0  # Default to 0, adjust logic if needed
        
        # Product category encoding
        product_categories = ['Dairy', 'Frozen', 'Household', 'Snack']
        for cat in product_categories:
            df[f'product_category_{cat}'] = (df['product_category'] == cat).astype(float)
        
        # Store location encoding
        store_locations = ['Los_Angeles', 'New_York']  # Note: using underscores to match model
        for loc in store_locations:
            # Handle space in location names
            original_loc = loc.replace('_', ' ')
            df[f'store_location_{loc}'] = (df['store_location'] == original_loc).astype(float)
        
        # Weekday encoding
        weekdays = ['Monday', 'Saturday', 'Thursday', 'Tuesday', 'Wednesday']
        for day in weekdays:
            df[f'weekday_{day}'] = (df['weekday'] == day).astype(float)
        
        # Drop original categorical columns and temporary columns
        df = df.drop(columns=['product_category', 'store_location', 'date', 'weekday'], errors='ignore')
        
        # Ensure we have all expected features in correct order
        expected_features = [
            'price', 'stock_available', 'store_id_str_02', 'store_id_str_03',
            'product_id_pdt_002', 'product_id_pdt_003', 'product_id_pdt_004', 
            'product_id_pdt_005', 'product_category_Dairy', 'product_category_Frozen',
            'product_category_Household', 'product_category_Snack',
            'store_location_Los_Angeles', 'store_location_New_York',
            'weekday_Monday', 'weekday_Saturday', 'weekday_Thursday', 
            'weekday_Tuesday', 'weekday_Wednesday', 'revenue', 'day', 'month', 'year'
        ]
        
        # Check if model has feature names
        if hasattr(model, 'feature_names_in_'):
            expected_features = model.feature_names_in_.tolist()
            print("Model expects features:", expected_features)
        
        # Reindex to ensure correct feature order and fill missing with 0
        df = df.reindex(columns=expected_features, fill_value=0.0)
        
        print("🔄 Final data shape:", df.shape)
        print("🔄 Final columns:", df.columns.tolist())
        print("🔄 Final values:", df.values)
        
        # Make prediction
        prediction = model.predict(df)
        print("✅ Prediction successful:", prediction)
        return prediction
        
    except Exception as e:
        print("❌ Prediction failed:", str(e))
        import traceback
        traceback.print_exc()
        raise e