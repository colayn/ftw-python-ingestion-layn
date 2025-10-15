import requests
import pandas as pd

# --- Step 1. Define the base URL ---
BASE_URL = "https://api.open-meteo.com/v1/forecast"

# --- Step 2. Set up the request parameters (payload) ---
params = {
    "latitude": 14.6,             # Manila latitude
    "longitude": 121.0,           # Manila longitude
    "current": "temperature_2m",  # which variable(s) we want to retrieve
    # optional extras you could include:
    # "timezone": "Asia/Manila",
    # "forecast_days": 1
}

# --- Step 3. Send the GET request with parameters ---
response = requests.get(BASE_URL, params=params)

# Let's inspect the final URL
print(response.url)

# --- Step 4. Convert the response to JSON ---
data = response.json()
# print(f"data: {data}")
print(data)

# --- Step 5. Normalize the nested JSON into a flat table ---
print(data)
df = pd.json_normalize(data)

# --- Step 6. Inspect the results ---
print(df.head())

# Let's save to output in CSV
df.to_csv("output/meteo_sample.csv", index=False)