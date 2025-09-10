import os
import time
import requests

def get_temperature(city):
    try:
        print(f"[DEBUG] Looking up coordinates for city: {city}", flush=True)
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_res = requests.get(geo_url, timeout=10).json()

        if "results" not in geo_res:
            print(f"[ERROR] No results found for city: {city}", flush=True)
            return None, None

        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]
        print(f"[DEBUG] Got coordinates for {city}: lat={lat}, lon={lon}", flush=True)import os
import time
import requests
import paho.mqtt.client as mqtt

# MQTT Setup
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")   # e.g. "192.168.1.100"
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "weather/temperature")

client = mqtt.Client()
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print(f"[INFO] Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}", flush=True)
except Exception as e:
    print(f"[ERROR] Could not connect to MQTT broker: {e}", flush=True)


def get_temperature(city):
    try:
        print(f"[DEBUG] Looking up coordinates for city: {city}", flush=True)
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_res = requests.get(geo_url, timeout=10).json()

        if "results" not in geo_res:
            print(f"[ERROR] No results found for city: {city}", flush=True)
            return None, None

        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]
        print(f"[DEBUG] Got coordinates for {city}: lat={lat}, lon={lon}", flush=True)

        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        data = requests.get(url, timeout=10).json()

        if "current_weather" not in data:
            print(f"[ERROR] Weather data not found for city: {city}", flush=True)
            return None, None

        return data["current_weather"]["temperature"], data["current_weather"]["time"]

    except Exception as e:
        print(f"[EXCEPTION] Failed to fetch temperature for {city}: {e}", flush=True)
        return None, None


print("[INFO] Starting weather app...", flush=True)

city = os.getenv("CITY", "Hyderabad")   # Default city if not provided
print(f"[INFO] Using city: {city}", flush=True)

last_temp = None

while True:
    temp, ts = get_temperature(city)
    if temp is not None:
        if temp != last_temp:
            msg = f"[{ts}] Current temperature in {city}: {temp}°C"
            print(f"[INFO] {msg}", flush=True)

            # Publish to MQTT broker
            try:
                client.publish(MQTT_TOPIC, msg)
                print(f"[DEBUG] Published to {MQTT_TOPIC}", flush=True)
            except Exception as e:
                print(f"[ERROR] Failed to publish MQTT message: {e}", flush=True)

            last_temp = temp
        else:
            print(f"[DEBUG] No change in temperature. Still {temp}°C", flush=True)
    else:
        print("[WARN] Skipping update due to error.", flush=True)

    time.sleep(30)


        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        data = requests.get(url, timeout=10).json()

        if "current_weather" not in data:
            print(f"[ERROR] Weather data not found for city: {city}", flush=True)
            return None, None

        return data["current_weather"]["temperature"], data["current_weather"]["time"]

    except Exception as e:
        print(f"[EXCEPTION] Failed to fetch temperature for {city}: {e}", flush=True)
        return None, None


print("[INFO] Starting weather app...", flush=True)

city = os.getenv("CITY", "Hyderabad")   # Default city if not provided
print(f"[INFO] Using city: {city}", flush=True)

last_temp = None

while True:
    temp, ts = get_temperature(city)
    if temp is not None:
        if temp != last_temp:
            print(f"[INFO] [{ts}] Current temperature in {city}: {temp}°C", flush=True)
            last_temp = temp
        else:
            print(f"[DEBUG] No change in temperature. Still {temp}°C", flush=True)
    else:
        print("[WARN] Skipping update due to error.", flush=True)

    time.sleep(30)
