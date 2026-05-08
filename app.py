from flask import Flask, render_template, request, jsonify
import requests
import json
import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")
CACHE_DURATION = 300  # 5 minutes
# Vercel serverless only allows writes in /tmp. Local dev keeps project cache dir.
if os.environ.get("VERCEL"):
    CACHE_DIR = "/tmp/mydarksky-cache"
else:
    CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")

try:
    os.makedirs(CACHE_DIR, exist_ok=True)
except OSError:
    # If directory creation fails (restricted filesystem), disable file cache safely.
    CACHE_DIR = None

# Check if API key is set
if not API_KEY:
    print("⚠️  WARNING: OPENWEATHER_API_KEY not set!")
    print("Get your free API key from: https://openweathermap.org/api")
    print("Set it in .env file or as environment variable")


def get_cache_key(cache_type, *args):
    return "_".join([cache_type] + [str(a).replace(" ", "_").replace(",", "") for a in args])


def get_cache(key):
    if not CACHE_DIR:
        return None
    path = os.path.join(CACHE_DIR, f"{key}.json")
    if os.path.exists(path):
        try:
            with open(path) as f:
                data = json.load(f)
            if time.time() - data["timestamp"] < CACHE_DURATION:
                return data["payload"]
        except (OSError, json.JSONDecodeError, KeyError, TypeError):
            return None
    return None


def set_cache(key, payload):
    if not CACHE_DIR:
        return
    path = os.path.join(CACHE_DIR, f"{key}.json")
    try:
        with open(path, "w") as f:
            json.dump({"timestamp": time.time(), "payload": payload}, f)
    except OSError:
        # Cache write failures should not fail API responses.
        return


def fetch_current(lat, lon):
    key = get_cache_key("current", lat, lon)
    cached = get_cache(key)
    if cached:
        return cached
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    set_cache(key, data)
    return data


def fetch_forecast(lat, lon):
    key = get_cache_key("forecast", lat, lon)
    cached = get_cache(key)
    if cached:
        return cached
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial&cnt=40"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    set_cache(key, data)
    return data


def fetch_historical(lat, lon, dt):
    key = get_cache_key("history", lat, lon, dt)
    cached = get_cache(key)
    if cached:
        return cached
    url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={dt}&appid={API_KEY}&units=imperial"
    r = requests.get(url, timeout=10)
    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        if r.status_code == 401:
            raise PermissionError(
                "Historical weather is not enabled for this OpenWeather API key "
                "(One Call Time Machine requires a supported subscription)."
            ) from e
        raise
    data = r.json()
    set_cache(key, data)
    return data


def select_forecast_for_date(raw_forecast, target_date):
    items = raw_forecast.get("list", [])
    if not items:
        return None

    best_item = None
    best_delta = None
    for item in items:
        item_dt = datetime.fromtimestamp(item["dt"])
        if item_dt.date() != target_date.date():
            continue

        noon = target_date.replace(hour=12, minute=0, second=0, microsecond=0)
        delta = abs((item_dt - noon).total_seconds())
        if best_delta is None or delta < best_delta:
            best_delta = delta
            best_item = item

    return best_item


def geocode(query):
    key = get_cache_key("geo", query)
    cached = get_cache(key)
    if cached:
        return cached
    url = f"https://api.openweathermap.org/geo/1.0/direct?q={query}&limit=1&appid={API_KEY}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    if data:
        result = {"lat": data[0]["lat"], "lon": data[0]["lon"], "name": data[0].get("name", query), "country": data[0].get("country", "")}
        set_cache(key, result)
        return result
    return None


def reverse_geocode(lat, lon):
    key = get_cache_key("revgeo", lat, lon)
    cached = get_cache(key)
    if cached:
        return cached
    url = f"https://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={API_KEY}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    if data:
        result = {"name": data[0].get("name", ""), "country": data[0].get("country", "")}
        set_cache(key, result)
        return result
    return {"name": "Unknown", "country": ""}


def process_forecast(raw):
    days = {}
    for item in raw.get("list", []):
        dt = datetime.fromtimestamp(item["dt"])
        day_key = dt.strftime("%Y-%m-%d")
        if day_key not in days:
            days[day_key] = {
                "date": day_key,
                "day_name": dt.strftime("%a"),
                "full_date": dt.strftime("%B %d"),
                "temps": [],
                "icons": [],
                "descriptions": [],
                "humidity": [],
                "wind": [],
            }
        days[day_key]["temps"].append(item["main"]["temp"])
        days[day_key]["icons"].append(item["weather"][0]["icon"])
        days[day_key]["descriptions"].append(item["weather"][0]["description"])
        days[day_key]["humidity"].append(item["main"]["humidity"])
        days[day_key]["wind"].append(item["wind"]["speed"])

    result = []
    for day_key, d in sorted(days.items())[:8]:
        icon_counts = {}
        for ic in d["icons"]:
            icon_counts[ic] = icon_counts.get(ic, 0) + 1
        main_icon = max(icon_counts, key=icon_counts.get)
        result.append({
            "date": d["date"],
            "day_name": d["day_name"],
            "full_date": d["full_date"],
            "low": round(min(d["temps"])),
            "high": round(max(d["temps"])),
            "icon": main_icon,
            "description": d["descriptions"][0].title(),
            "humidity": round(sum(d["humidity"]) / len(d["humidity"])),
            "wind": round(sum(d["wind"]) / len(d["wind"])),
        })
    return result


def weather_icon_class(icon_code):
    mapping = {
        "01d": "sun", "01n": "moon",
        "02d": "cloud-sun", "02n": "cloud-moon",
        "03d": "cloud", "03n": "cloud",
        "04d": "clouds", "04n": "clouds",
        "09d": "cloud-rain", "09n": "cloud-rain",
        "10d": "cloud-sun-rain", "10n": "cloud-moon-rain",
        "11d": "cloud-lightning", "11n": "cloud-lightning",
        "13d": "snowflake", "13n": "snowflake",
        "50d": "wind", "50n": "wind",
    }
    return mapping.get(icon_code, "cloud")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/weather")
def api_weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    query = request.args.get("q")

    try:
        if query:
            geo = geocode(query)
            if not geo:
                return jsonify({"error": "Location not found"}), 404
            lat, lon = geo["lat"], geo["lon"]
            location_name = f"{geo['name']}, {geo['country']}"
        elif lat and lon:
            lat, lon = float(lat), float(lon)
            rev = reverse_geocode(lat, lon)
            location_name = f"{rev['name']}, {rev['country']}"
        else:
            return jsonify({"error": "No location provided"}), 400

        current = fetch_current(lat, lon)
        forecast_raw = fetch_forecast(lat, lon)
        forecast = process_forecast(forecast_raw)

        weather = current["weather"][0]
        main = current["main"]
        wind = current["wind"]

        return jsonify({
            "location": location_name,
            "lat": lat,
            "lon": lon,
            "current": {
                "temp": round(main["temp"]),
                "feels_like": round(main["feels_like"]),
                "humidity": main["humidity"],
                "pressure": main["pressure"],
                "visibility": round(current.get("visibility", 0) / 1609.34, 1),
                "wind_speed": round(wind["speed"]),
                "wind_deg": wind.get("deg", 0),
                "description": weather["description"].title(),
                "icon": weather["icon"],
                "icon_class": weather_icon_class(weather["icon"]),
                "dew_point": round(main["temp"] - ((100 - main["humidity"]) / 5)),
                "uv_index": 0,
                "sunrise": datetime.fromtimestamp(current["sys"]["sunrise"]).strftime("%H:%M"),
                "sunset": datetime.fromtimestamp(current["sys"]["sunset"]).strftime("%H:%M"),
            },
            "forecast": forecast,
        })
    except requests.HTTPError as e:
        return jsonify({"error": f"Weather API error: {e}"}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/historical")
def api_historical():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    date_str = request.args.get("date")

    try:
        lat, lon = float(lat), float(lon)
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        now = datetime.now()

        if dt.date() == now.date():
            current = fetch_current(lat, lon)
            weather = current.get("weather", [{}])[0]
            main = current.get("main", {})
            wind = current.get("wind", {})
            return jsonify({
                "date": date_str,
                "source": "current",
                "temp": round(main.get("temp", 0)),
                "feels_like": round(main.get("feels_like", 0)),
                "humidity": main.get("humidity", 0),
                "wind_speed": round(wind.get("speed", 0)),
                "description": weather.get("description", "").title(),
                "icon": weather.get("icon", "03d"),
                "icon_class": weather_icon_class(weather.get("icon", "03d")),
            })

        if dt.date() < now.date():
            timestamp = int(dt.timestamp())
            try:
                data = fetch_historical(lat, lon, timestamp)
            except PermissionError as e:
                return jsonify({"error": str(e)}), 402
            current = data.get("current") or data.get("data", [{}])[0]

            weather = current.get("weather", [{}])[0]
            return jsonify({
                "date": date_str,
                "source": "historical",
                "temp": round(current.get("temp", 0)),
                "feels_like": round(current.get("feels_like", 0)),
                "humidity": current.get("humidity", 0),
                "wind_speed": round(current.get("wind_speed", 0)),
                "description": weather.get("description", "").title(),
                "icon": weather.get("icon", "03d"),
                "icon_class": weather_icon_class(weather.get("icon", "03d")),
            })

        forecast_raw = fetch_forecast(lat, lon)
        selected = select_forecast_for_date(forecast_raw, dt)
        if not selected:
            return jsonify({
                "error": "Selected future date is out of forecast range (about 5 days)."
            }), 400

        weather = selected.get("weather", [{}])[0]
        main = selected.get("main", {})
        wind = selected.get("wind", {})
        return jsonify({
            "date": date_str,
            "source": "forecast",
            "temp": round(main.get("temp", 0)),
            "feels_like": round(main.get("feels_like", 0)),
            "humidity": main.get("humidity", 0),
            "wind_speed": round(wind.get("speed", 0)),
            "description": weather.get("description", "").title(),
            "icon": weather.get("icon", "03d"),
            "icon_class": weather_icon_class(weather.get("icon", "03d")),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
