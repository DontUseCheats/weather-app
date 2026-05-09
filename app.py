import os
import requests
from flask import Flask, request, render_template
from dotenv import load_dotenv
from timezonefinder import TimezoneFinder

app = Flask(__name__)
load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")

# homepage route
@app.route("/")
def index():
    return render_template("index.html")

# inputted location route
@app.route("/weather", methods=["POST"])
def weather():
    user_location = request.form["user_location"]
    url, params = set_city_or_zip(user_location)
    lat, lon = get_location(url, params, user_location)
    current_temperature, timezone_name = get_weather(lat, lon)
    return render_template("weather.html", temperature = current_temperature)


def set_city_or_zip(user_location):
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
    return url, params

def get_location(received_url, params, received_user_location):
    find_user_location = requests.get(received_url, params=params)

    if received_user_location.isdigit():
        location = find_user_location.json()
    else:
        location = find_user_location.json()[0]
    return location["lat"], location["lon"]

def get_weather(lat, lon):
    response = requests.get("https://api.openweathermap.org/data/2.5/weather", params={
        "lat": lat,
        "lon": lon,
        "units": "imperial",
        "appid": api_key
    })

    data = response.json()

    tf = TimezoneFinder()
    current_temperature = data["main"]["temp"]
    timezone_name = tf.timezone_at(lat=lat, lng=lon)
    return current_temperature, timezone_name


if __name__ == "__main__":
    app.run