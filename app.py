import os
import time
import requests

def get_temperature(city):
    # Use geocoding API to convert city -> lat/lon
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    geo_res = requests.get(geo_url).json()
    if "results" not in geo_res:
        return None, None
    lat = geo_res["results"][0]["latitude"]
    lon = geo_res["results"][0]["longitude"]

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    data = requests.get(url).json()
    return data["current_weather"]["temperature"], data["current_weather"]["time"]

city = os.getenv("CITY", "Hyderabad")   # default Hyderabad

last_temp = None
while True:
    temp, ts = get_temperature(city)
    if temp is not None and temp != last_temp:
        print(f"[{ts}] Current temperature in {city}: {temp}°C")
        last_temp = temp
    time.sleep(30)
