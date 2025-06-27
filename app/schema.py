from pydantic import BaseModel, validator
from typing import Union

class SalesInput(BaseModel):
    price: float
    stock_available: float
    day: int
    month: int
    year: int
    product_category: str
    store_location: str
    
    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v
    
    @validator('stock_available')
    def validate_stock(cls, v):
        if v < 0:
            raise ValueError('Stock available must be non-negative')
        return v
    
    @validator('day')
    def validate_day(cls, v):
        if not 1 <= v <= 31:
            raise ValueError('Day must be between 1 and 31')
        return v
    
    @validator('month')
    def validate_month(cls, v):
        if not 1 <= v <= 12:
            raise ValueError('Month must be between 1 and 12')
        return v
    
    @validator('year')
    def validate_year(cls, v):
        if v < 1900:
            raise ValueError('Year must be after 1900')
        return v
    
    @validator('product_category')
    def validate_category(cls, v):
        valid_categories = ['Beverage', 'Dairy', 'Frozen', 'Household', 'Snack']
        if v not in valid_categories:
            raise ValueError(f'Product category must be one of: {valid_categories}')
        return v
    
    @validator('store_location')
    def validate_location(cls, v):
        valid_locations = ['Los Angeles', 'New York', 'Chicago']
        if v not in valid_locations:
            raise ValueError(f'Store location must be one of: {valid_locations}')
        return v