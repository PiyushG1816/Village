from flask import Flask, render_template
import pandas as pd
import requests

app = Flask(__name__,template_folder='template')

# Function to get the current temperature from OpenWeatherMap API
def get_current_temperature(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temp_kelvin = data["main"]["temp"]
        temp_fahrenheit = (temp_kelvin - 273.15) * 9/5 + 32  # Convert Kelvin to Fahrenheit
        return round(temp_fahrenheit, 2)
    else:
        return "Error fetching temperature"

# Route to display menu and additional info
@app.route("/")
def index():
    # Load menu CSV data
    menu_file = "menu_data.csv"  # Replace with your menu CSV file path
    menu_df = pd.read_csv(menu_file)
    menu_items = menu_df.to_dict(orient="records")

    # Extract restaurant info
    restaurant_info = {
        "name": menu_df.iloc[0]["Restaurant"],
        "address": menu_df.iloc[0]["Address"],
        "opening_hours": menu_df.iloc[0]["Opening Hours"],
        "holiday": menu_df.iloc[0]["Holiday"]
    }

    # Load busy timings from CSV
    busy_file = "busy_times.csv"  # Replace with your busy timing file path
    busy_df = pd.read_csv(busy_file, index_col=0)  # Assuming days are rows, time slots are columns
    if restaurant_info["holiday"] in busy_df.index:
        busy_df = busy_df.drop(restaurant_info["holiday"])
    busy_timings = busy_df.to_dict(orient="index")
    time_slots = busy_df.columns.tolist()
    # Get current temperature
    city = "Hicksville"  # Replace with your restaurant's city
    api_key = "Your_api_key"  # Replace with your API key
    temperature = get_current_temperature(api_key, city)

    return render_template(
        "index.html",
        menu_items=menu_items,
        restaurant_info=restaurant_info,
        busy_timings=busy_timings,
        time_slots=time_slots,
        current_temperature=temperature,
    )

if __name__ == "__main__":
    app.run(debug=True)
