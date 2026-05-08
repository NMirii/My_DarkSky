# My Dark Sky - Weather Forecast Application

A beautiful weather application inspired by the original Dark Sky, featuring current weather, 8-day forecasts, and a time machine to explore historical weather data.

## Features

- 🌤️ **Current Weather** - Real-time weather conditions
- 📍 **Location Search** - Search any city or use current location
- 📅 **8-Day Forecast** - Extended weather predictions
- ⏳ **Time Machine** - Explore past and future weather
- 💾 **Smart Caching** - 5-minute cache system for faster responses
- 🎨 **Beautiful UI** - Dark Sky-inspired design with Tailwind CSS

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: Tailwind CSS, Vanilla JavaScript
- **API**: OpenWeather API
- **Caching**: JSON file-based cache

## Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Get your OpenWeather API key from [https://openweathermap.org/api](https://openweathermap.org/api)

4. Create a `.env` file:
   ```bash
   cp .env.example .env
   ```
   
5. Add your API key to `.env`:
   ```
   OPENWEATHER_API_KEY=your_actual_api_key
   ```

6. Run the app:
   ```bash
   python app.py
   ```

7. Open [http://localhost:5000](http://localhost:5000)

## Deployment Options

### Option 1: Render

1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn app:app`
5. Add environment variable: `OPENWEATHER_API_KEY`
6. Deploy!

### Option 2: Railway

1. Create a new project on [Railway](https://railway.app)
2. Connect your GitHub repository
3. Add environment variable: `OPENWEATHER_API_KEY`
4. Railway auto-detects Flask and deploys

### Option 3: Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create mydarksky-app`
4. Set API key: `heroku config:set OPENWEATHER_API_KEY=your_key`
5. Deploy: `git push heroku main`

### Option 4: Netlify (with serverless functions)

Requires adapting Flask routes to serverless functions. See Netlify Functions documentation.

### Option 5: Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Create `vercel.json`:
   ```json
   {
     "builds": [{"src": "app.py", "use": "@vercel/python"}],
     "routes": [{"src": "/(.*)", "dest": "app.py"}]
   }
   ```
3. Deploy: `vercel --prod`
4. Add environment variable in Vercel dashboard

## Environment Variables

- `OPENWEATHER_API_KEY` - Your OpenWeather API key (required)
- `FLASK_ENV` - Set to `production` for deployment

## API Endpoints

- `GET /` - Main application
- `GET /api/weather?lat={lat}&lon={lon}` - Get weather by coordinates
- `GET /api/weather?q={city}` - Get weather by city name
- `GET /api/historical?lat={lat}&lon={lon}&date={YYYY-MM-DD}` - Historical weather

## Cache System

The application implements a 5-minute JSON-based cache:
- Reduces API calls to OpenWeather
- Improves response times
- Cache files stored in `cache/` directory
- Automatic cache invalidation after 5 minutes

## License

MIT License - feel free to use and modify!

## Credits

Inspired by the original Dark Sky application by The Dark Sky Company (acquired by Apple).
