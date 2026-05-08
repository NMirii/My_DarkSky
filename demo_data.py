# Demo Mode - For testing without API key
# This file provides sample weather data when OPENWEATHER_API_KEY is not set

DEMO_DATA = {
    "location": "New York, US",
    "lat": 40.7128,
    "lon": -74.0060,
    "current": {
        "temp": 45,
        "feels_like": 42,
        "humidity": 65,
        "pressure": 1013,
        "visibility": 10.0,
        "wind_speed": 12,
        "wind_deg": 220,
        "description": "Partly Cloudy",
        "icon": "02d",
        "icon_class": "cloud-sun",
        "dew_point": 35,
        "uv_index": 3,
        "sunrise": "06:30",
        "sunset": "18:45"
    },
    "forecast": [
        {
            "date": "2024-05-07",
            "day_name": "Today",
            "full_date": "May 7",
            "low": 40,
            "high": 55,
            "icon": "02d",
            "description": "Partly Cloudy",
            "humidity": 65,
            "wind": 12
        },
        {
            "date": "2024-05-08",
            "day_name": "Thu",
            "full_date": "May 8",
            "low": 42,
            "high": 58,
            "icon": "10d",
            "description": "Light Rain",
            "humidity": 75,
            "wind": 15
        },
        {
            "date": "2024-05-09",
            "day_name": "Fri",
            "full_date": "May 9",
            "low": 38,
            "high": 52,
            "icon": "03d",
            "description": "Cloudy",
            "humidity": 70,
            "wind": 10
        },
        {
            "date": "2024-05-10",
            "day_name": "Sat",
            "full_date": "May 10",
            "low": 35,
            "high": 48,
            "icon": "13d",
            "description": "Light Snow",
            "humidity": 80,
            "wind": 8
        },
        {
            "date": "2024-05-11",
            "day_name": "Sun",
            "full_date": "May 11",
            "low": 40,
            "high": 55,
            "icon": "01d",
            "description": "Clear Sky",
            "humidity": 50,
            "wind": 7
        },
        {
            "date": "2024-05-12",
            "day_name": "Mon",
            "full_date": "May 12",
            "low": 45,
            "high": 62,
            "icon": "02d",
            "description": "Few Clouds",
            "humidity": 55,
            "wind": 9
        },
        {
            "date": "2024-05-13",
            "day_name": "Tue",
            "full_date": "May 13",
            "low": 48,
            "high": 65,
            "icon": "01d",
            "description": "Sunny",
            "humidity": 45,
            "wind": 6
        },
        {
            "date": "2024-05-14",
            "day_name": "Wed",
            "full_date": "May 14",
            "low": 50,
            "high": 68,
            "icon": "02d",
            "description": "Mostly Sunny",
            "humidity": 50,
            "wind": 8
        }
    ]
}
