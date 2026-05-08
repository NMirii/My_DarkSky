# Welcome to My Dark Sky
***

## Task
The goal of this project is to recreate a Dark Sky-style weather app using Python and Flask with a modern, beautiful UI.
The challenge is combining multiple requirements in one app:
- current location and searched location support
- current weather and multi-day forecast
- date-based weather lookup for past/future behavior
- API rate-limit friendly caching for 5 minutes
- cloud deployment with a public URL

## Description
I solved the task by building a Flask backend with OpenWeather integration and a Tailwind-based frontend.

Main implementation points:
- Built `GET /api/weather` for live weather and forecast by coordinates or search query
- Built `GET /api/historical` for date-based weather:
  - today uses current weather
  - past dates use historical endpoint (if API plan supports it)
  - future dates use forecast endpoint for nearest available date
- Added JSON file cache with a 5-minute TTL to reduce repeated external API calls
- Added Vercel-safe cache handling (`/tmp` in serverless runtime) to prevent deployment crashes
- Designed a polished Dark Sky-inspired interface with location search, geolocation button, forecast cards, and a time machine section

## Installation
```bash
pip install -r requirements.txt
```

Create `.env` file:
```bash
cp .env.example .env
```

Add your API key:
```env
OPENWEATHER_API_KEY=your_api_key_here
```

## Usage
Run locally:
```bash
python app.py
```

Open in browser:
```text
http://localhost:5000
```
You can also look project: https://my-dark-sky-gamma.vercel.app/

Use the app:
- search for a city in the search bar
- click the location button to use your current position
- choose a date in Time Machine to view date-based weather

### The Core Team


<span><i>Made at <a href='https://qwasar.io'>Qwasar SV -- Software Engineering School</a></i></span>
<span><img alt='Qwasar SV -- Software Engineering School's Logo' src='https://storage.googleapis.com/qwasar-public/qwasar-logo_50x50.png' width='20px' /></span>
