import requests

# API details
api_key = "Your_AP_Key"  # Replace with your OpenWeatherMap API key
latitude = 40.76665603  # Replace with actual latitude
longitude = -73.52353817  # Replace with actual longitude
url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"

# Fetch weather data
response = requests.get(url)
if response.status_code == 200:
    weather_data = response.json()
    # Extract temperature and rain details
    temperature = weather_data['main']['temp']
    rain = weather_data.get('rain', {}).get('1h', 0)  # Rainfall in the last hour (mm)
    print(f"Current Temperature: {temperature}°C")
    print(f"Rain in the last hour: {rain} mm")
else:
    print(f"Failed to fetch data. HTTP Status code: {response.status_code}")
