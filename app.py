from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

# Load model and columns
model = joblib.load("equitylens_model_compressed.pkl")
feature_columns = joblib.load("feature_columns.pkl")

app = FastAPI()

# Input schema
class PropertyInput(BaseModel):
    rooms: int
    area: float
    district: str
    house_type: str
    year_built: int
    floor: float
    total_floors: float
    latitude: float
    longitude: float

# Prediction function
def predict_price(input_data):

    input_df = pd.DataFrame([input_data])

    input_df = pd.get_dummies(
        input_df,
        columns=["district", "house_type"]
    )

    input_df = input_df.reindex(
        columns=feature_columns,
        fill_value=0
    )

    predicted_price = model.predict(input_df)[0]

    return predicted_price

# Rent estimation
def estimate_rent(predicted_price):

    monthly_rent = predicted_price * 0.005

    return monthly_rent

# Sell vs rent logic
def compare_sell_vs_rent(predicted_price, monthly_rent, years=10):

    selling_cost_rate = 0.03
    vacancy_rate = 0.08
    maintenance_rate = 0.01

    net_sale = predicted_price * (1 - selling_cost_rate)

    annual_rent = monthly_rent * 12
    adjusted_rent = annual_rent * (1 - vacancy_rate)

    annual_maintenance = predicted_price * maintenance_rate

    net_annual_rent = adjusted_rent - annual_maintenance

    total_rent_income = net_annual_rent * years

    if total_rent_income > net_sale:
        recommendation = "Renting may be more profitable long-term."
    else:
        recommendation = "Selling may be more profitable."

    return {
        "net_sale": round(net_sale),
        "monthly_rent": round(monthly_rent),
        "total_rent_income": round(total_rent_income),
        "recommendation": recommendation
    }

# API endpoint
@app.post("/predict")
def predict(property_data: PropertyInput):

    input_data = property_data.dict()

    predicted_price = predict_price(input_data)

    predicted_price_usd = predicted_price / 500

    monthly_rent = estimate_rent(predicted_price)

    result = compare_sell_vs_rent(
        predicted_price,
        monthly_rent
    )

    return {
        "predicted_price_kzt": round(predicted_price),
        "predicted_price_usd": round(predicted_price_usd),
        "estimated_monthly_rent_kzt": round(monthly_rent),
        "recommendation": result["recommendation"],
        "total_10_year_rent_income_kzt": result["total_rent_income"]
    }