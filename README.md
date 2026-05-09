# EquityLens AI

EquityLens is an AI-powered real estate decision assistant that predicts property sale price, estimates monthly rental income, and compares long-term selling vs renting profitability.

## Project Overview

This project was built as a machine learning MVP for real estate decision support.  
The system uses historical real estate listing data from Astana to estimate property value based on user-provided features such as area, number of rooms, district, house type, year built, floor, and optional geographic coordinates.

## Features

- Predicts property sale price in KZT
- Converts estimated price to USD
- Estimates monthly rental income
- Calculates 10-year rental income
- Provides a sell vs rent recommendation
- Frontend built with Lovable
- Backend built with FastAPI
- ML model deployed through Render

## Dataset

The model was trained on an Astana real estate dataset containing approximately 18,293 property listings.

Selected features:
- rooms
- area
- district
- house_type
- year_built
- floor
- total_floors
- latitude
- longitude

Target variable:
- price_kzt

## Machine Learning Approach

This is a supervised regression problem.  
The model predicts a continuous numerical value: property sale price.

Model used:

```text
RandomForestRegressor
