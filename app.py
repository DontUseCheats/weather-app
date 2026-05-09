import os
import requests
from flask import Flask, request, render_template
from dotenv import load_dotenv
from timezonefinder import TimezoneFinder

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

tf = TimezoneFinder()

load_dotenv()

api_key = os.getenv("WEATHER_API_KEY")

user_location = input("Enter city or zip code: ")

if user_location.isdigit():
    url = "http://api.openweathermap.org/geo/1.0/zip"
    params = {
        "zip": user_location,
        "appid": api_key
        }
else:
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": user_location,
        "appid": api_key
        }

find_user_location = requests.get(url, params=params)

if user_location.isdigit():
    location = find_user_location.json()
else:
    location = find_user_location.json()[0]

lat = location["lat"]
lon = location["lon"]

response = requests.get("https://api.openweathermap.org/data/2.5/weather", params={
    "lat": lat,
    "lon": lon,
    "units": "imperial",
    "appid": api_key
})

data = response.json()

current_temperature = data["main"]["temp"]
timezone_name = tf.timezone_at(lat=lat, lng=lon)


if __name__ == "__main__":
    app.run