import requests
import time

def get_coordinates(city_name):
    """Convert city name to latitude and longitude using Open-Meteo Geocoding API."""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
    response = requests.get(url).json()
    if "results" in response and len(response["results"]) > 0:
        lat = response["results"][0]["latitude"]
        lon = response["results"][0]["longitude"]
        return lat, lon
    else:
        raise ValueError("City not found!")

# Ask user for location
city = input("Enter city name: ")
lat, lon = get_coordinates(city)
print(f"Coordinates for {city}: {lat}, {lon}")

# Open-Meteo API URL
URL = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"

last_temp = None  # to store previous temperature

while True:
    try:
        response = requests.get(URL)
        data = response.json()
        temp = data["hourly"]["temperature_2m"][0]

        if last_temp is None or temp != last_temp:
            print(f"{time.ctime()}: Current temperature in {city}: {temp}°C")
            with open("/app/temperature.txt", "a") as f:
                f.write(f"{time.ctime()}: {city}: {temp}°C\n")
            last_temp = temp  # update last_temp

    except Exception as e:
        print("Error fetching temperature:", e)

    time.sleep(60)  # fetch every 60 seconds

