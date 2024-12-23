import pandas as pd
import requests
from datetime import datetime

# File paths
menu_file = "menu_data.csv"
busy_times_file = "busy_times.csv"

# OpenWeatherMap API details
api_key = "125893d0d74c6bda2b6a9c9abdd7f8ef"
latitude = 40.76665603  # Replace with actual latitude
longitude = 73.52353817  # Replace with actual longitude
weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"

# Fetch current weather data
response = requests.get(weather_url)
if response.status_code == 200:
    weather_data = response.json()
    rain = weather_data.get('rain', {}).get('1h', 0)  # Rain in the last hour (mm)
    weather_condition = weather_data['weather'][0]['main']  # e.g., "Rain", "Clear"
else:
    print("Failed to fetch weather data")
    rain = 0
    weather_condition = "Unknown"

# Load menu prices
menu_df = pd.read_csv(menu_file)  # Assumes columns: "Item", "Base Price"

# Load busy times data
busy_times_df = pd.read_csv(busy_times_file)  # Rows: Days, Columns: Time Slots

# Get current day and time slot
current_day = datetime.now().strftime("%A")  # e.g., "Monday"
current_time = datetime.now().strftime("%I:%M %p")  # e.g., "07:00 PM"

# Match the busy percentage for the current day and time slot
if current_time in busy_times_df.columns:
    busy_percentage = busy_times_df.loc[busy_times_df["Day"] == current_day, current_time].values
    if len(busy_percentage) > 0:
        busy_percentage = busy_percentage[0]
    else:
        busy_percentage = 50  # Default to 50% if no data is found
else:
    busy_percentage = 50  # Default to 50% if the current time slot is missing

# Adjust prices
def adjust_price(base_price, busy_percentage, weather_condition, rain,temperature):
    adjusted_price = base_price
    # Adjust for busy times
    if busy_percentage >= 80:
        adjusted_price *= 1.2  # 20% increase for peak times
    elif busy_percentage >= 60:
        adjusted_price *= 1.1  # 10% increase for moderately busy times
    
    # Adjust for bad weather
    if weather_condition == "Rain" or rain > 0:
        adjusted_price *= 1.15  # 15% increase for bad weather

    if temperature <= 0:
        adjusted_price *= 1.1  # 10% increase for freezing temperatures
    return round(adjusted_price, 2)

menu_df["Adjusted Price"] = menu_df["Price"].apply(
    lambda x: adjust_price(x, busy_percentage, weather_condition, rain,weather_data['main']['temp'])
)

# Save the adjusted prices to a new CSV file
adjusted_prices_file = "adjusted_menu_prices.csv"
menu_df.to_csv(adjusted_prices_file, index=False)

print(f"Adjusted prices saved to {adjusted_prices_file}")
