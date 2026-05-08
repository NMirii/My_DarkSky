# Project Architecture

## Overview

My Dark Sky is a Flask-based weather application that provides current weather, forecasts, and historical weather data through a beautiful, Dark Sky-inspired interface.

## Technology Stack

### Backend
- **Flask**: Lightweight Python web framework
- **Requests**: HTTP library for API calls to OpenWeather
- **Python-dotenv**: Environment variable management
- **Gunicorn**: Production WSGI server

### Frontend
- **Tailwind CSS**: Utility-first CSS framework (via CDN)
- **Vanilla JavaScript**: No framework dependencies
- **Google Fonts**: DM Serif Display & DM Sans
- **CSS Animations**: Custom keyframe animations

### Data & Caching
- **JSON File Cache**: 5-minute cache for API responses
- **OpenWeather API**: Weather data provider

## Project Structure

```
mydarksky/
├── app.py                 # Main Flask application
├── demo_data.py          # Sample data for testing
├── requirements.txt      # Python dependencies
├── Procfile             # Heroku deployment config
├── runtime.txt          # Python version specification
├── vercel.json          # Vercel deployment config
├── .env.example         # Environment variable template
├── .gitignore           # Git ignore patterns
├── setup.sh             # Setup automation script
├── README.md            # User documentation
├── DEPLOYMENT.md        # Deployment guide
├── ARCHITECTURE.md      # This file
├── templates/
│   └── index.html       # Main frontend application
├── static/              # Static assets (empty, using CDN)
└── cache/               # JSON cache files (gitignored)
```

## Data Flow

### 1. User Request Flow

```
User Browser
    ↓
    → Search or Geolocation
    ↓
JavaScript (index.html)
    ↓
    → Fetch /api/weather?q=city or ?lat=X&lon=Y
    ↓
Flask Route (@app.route('/api/weather'))
    ↓
    → Check cache (get_cache)
    ↓
    ├─ Cache Hit → Return cached data
    └─ Cache Miss ↓
        ↓
        → OpenWeather API call
        ↓
        → Store in cache (set_cache)
        ↓
        → Process & return JSON
    ↓
JavaScript renders UI
```

### 2. Cache System

```python
Cache Key Format: "{type}_{param1}_{param2}"
Examples:
  - "current_40.7128_-74.0060"
  - "forecast_40.7128_-74.0060"
  - "geo_New_York"

Cache File Structure:
{
  "timestamp": 1715039472.3,  
  "payload": { ... }          
}

Cache Duration: 300 seconds (5 minutes)
```

### 3. API Endpoints

#### GET /
Returns the main HTML application

#### GET /api/weather
Fetches current weather and 8-day forecast

**Parameters:**
- `q` (string): City name (e.g., "New York", "London, UK")
- OR
- `lat` (float) & `lon` (float): Coordinates

**Response:**
```json
{
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
    "description": "Partly Cloudy",
    "icon": "02d",
    ...
  },
  "forecast": [...]
}
```

#### GET /api/historical
Fetches historical weather data (requires paid OpenWeather plan)

**Parameters:**
- `lat` (float): Latitude
- `lon` (float): Longitude
- `date` (string): Date in YYYY-MM-DD format

## Design System

### Color Palette
```css
--sky-deep: #0a0e1a       /* Dark background */
--sky-mid: #0d1b3e        /* Mid-tone gradient */
--sky-light: #1a2d6b      /* Light gradient */
--accent-blue: #4a9eff    /* Primary accent */
--accent-cyan: #00d4ff    /* Secondary accent */
--accent-gold: #ffd166    /* Time machine accent */
--rain-color: #6eb4f7     /* Rain animation */
--text-primary: #e8f0fe   /* Main text */
--text-secondary: #8ba3cc /* Secondary text */
```

### Typography
- **Display**: DM Serif Display (for headings, temperatures)
- **Body**: DM Sans (for UI text, labels)

### Animation System
1. **Starfield**: CSS background with radial gradients
2. **Rain Overlay**: JavaScript-generated animated raindrops
3. **Fade-in**: Staggered animation delays for content reveal
4. **Float**: Icon bobbing animation
5. **Pulse**: Loading indicator

## API Integration

### OpenWeather API Endpoints Used

1. **Current Weather**
   ```
   GET /data/2.5/weather
   ?lat={lat}&lon={lon}&appid={key}&units=imperial
   ```

2. **5-day Forecast**
   ```
   GET /data/2.5/forecast
   ?lat={lat}&lon={lon}&appid={key}&units=imperial&cnt=40
   ```

3. **Geocoding**
   ```
   GET /geo/1.0/direct
   ?q={city}&limit=1&appid={key}
   ```

4. **Reverse Geocoding**
   ```
   GET /geo/1.0/reverse
   ?lat={lat}&lon={lon}&limit=1&appid={key}
   ```

5. **Historical Data** (Paid)
   ```
   GET /data/3.0/onecall/timemachine
   ?lat={lat}&lon={lon}&dt={timestamp}&appid={key}&units=imperial
   ```

### Rate Limiting

Free Tier Limits:
- 1,000 calls/day
- 60 calls/minute

Our cache system reduces API calls by:
- Storing responses for 5 minutes
- Deduplicating requests for same location
- Estimated reduction: 70-80% fewer API calls

## Deployment Considerations

### Environment Variables
- `OPENWEATHER_API_KEY`: Required for production
- `FLASK_ENV`: Set to "production" for deployment

### Hosting Requirements
- Python 3.8+
- Writeable filesystem for cache directory
- ~50MB disk space
- ~256MB RAM minimum

### Recommended Platforms
1. **Render**: Best free tier, automatic HTTPS
2. **Railway**: Easiest setup, generous free tier
3. **Heroku**: Most mature, requires credit card
4. **Vercel**: Serverless, great for scale

## Performance Optimizations

1. **Caching**: 5-minute cache reduces API calls
2. **CDN Assets**: Tailwind & fonts from CDN
3. **Minimal Dependencies**: Only 4 Python packages
4. **Client-side Rendering**: Dynamic UI updates without page reload
5. **Lazy Loading**: Weather icons loaded on demand

## Security

1. **API Key Protection**: Stored in environment variables
2. **No Client-side API Key**: All API calls server-side
3. **Input Validation**: Query parameters validated before API calls
4. **Error Handling**: Graceful degradation on API failures
5. **HTTPS**: Enforced on all deployment platforms

## Future Enhancements

Potential improvements:
- [ ] User preferences (°F/°C, mph/km/h)
- [ ] Multiple saved locations
- [ ] Weather alerts and notifications
- [ ] Radar/satellite imagery
- [ ] Air quality index
- [ ] UV index tracking
- [ ] Dark/light theme toggle
- [ ] Mobile app (PWA)
- [ ] Weather widgets/embeds
- [ ] Social sharing features

## Testing

### Manual Testing Checklist
- [ ] Search by city name
- [ ] Use current location
- [ ] View 8-day forecast
- [ ] Try Time Machine (if API supports)
- [ ] Test on mobile
- [ ] Test on desktop
- [ ] Verify cache (check network tab)
- [ ] Test error handling (invalid city)

### Browser Compatibility
- Chrome/Edge: ✓ Fully supported
- Firefox: ✓ Fully supported
- Safari: ✓ Fully supported
- Mobile browsers: ✓ Responsive design

## License

MIT License - Free for personal and commercial use
