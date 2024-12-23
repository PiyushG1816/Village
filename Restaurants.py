import requests

# Your Google Places API Key
API_KEY = "Your_API_Key"

# Address latitude and longitude (can be derived from a geocoding API)
latitude = 40.7665  # Latitude for 11 W Marie St, Hicksville, NY
longitude = -73.5251  # Longitude for 11 W Marie St, Hicksville, NY
radius = 2000  # 2 km radius
keyword = "South Indian food"

# Google Places API Nearby Search Endpoint
url = f"https://maps.google.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&keyword={keyword}&key={API_KEY}"

# Send request
response = requests.get(url)
data = response.json()

# Extract and sort top 5 restaurants by rating
if "results" in data:
    restaurants = sorted(data["results"], key=lambda x: x.get("rating", 0), reverse=True)[:5]

    for restaurant in restaurants:
        name = restaurant.get("name")
        address = restaurant.get("vicinity")
        rating = restaurant.get("rating")
        print(f"Name: {name}, Address: {address}, Rating: {rating}")
else:
    print("No restaurants found.")
