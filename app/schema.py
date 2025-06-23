from pydantic import BaseModel

class SalesInput(BaseModel):
    price: float
    stock_available: float
    store_id_str_02: float
    store_id_str_03: float
    product_id_pdt_002: float
    product_id_pdt_003: float
    product_id_pdt_004: float
    product_id_pdt_005: float
    product_category_Dairy: float
    product_category_Frozen: float
    product_category_Household: float
    product_category_Snack: float
    store_location_Los_Angeles: float
    store_location_New_York: float
    weekday_Monday: float
    weekday_Saturday: float
    weekday_Thursday: float
    weekday_Tuesday: float
    weekday_Wednesday: float
    revenue: float
    day: float
    month: float
    year: float
