import requests

def get_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m,relative_humidity_2m"
    }

    response = requests.get(url, params=params)
    data = response.json()
    current = data["current"]

    return current

manila_weather = get_weather(14.5995, 120.9842)
cebu_weather = get_weather(10.1800, 123.5300)
print(f"Temperature in Manila: {manila_weather['temperature_2m']}°C")
print(f"Humidity in Manila: {manila_weather['relative_humidity_2m']}%")
print(f"Wind speed in Manila: {manila_weather['wind_speed_10m']} km/h")
print('-----------------------------------------------------------')
print(f"Temperature in Cebu: {cebu_weather['temperature_2m']}°C")
print(f"Humidity in Cebu: {cebu_weather['relative_humidity_2m']}%")
print(f"Wind speed in Cebu: {cebu_weather['wind_speed_10m']} km/h")