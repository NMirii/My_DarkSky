# 🌤️ My Dark Sky - Quick Start Guide

## What You Have

A complete, production-ready weather application inspired by the original Dark Sky, featuring:

✅ Beautiful, responsive UI with animations
✅ Current weather conditions  
✅ 8-day forecast with visual temperature bars
✅ Time Machine to explore past/future weather
✅ Smart 5-minute caching system
✅ Location search and geolocation
✅ Ready to deploy to multiple platforms

## 3-Minute Setup

### Step 1: Get API Key (2 minutes)

1. Go to https://openweathermap.org/api
2. Click "Sign Up" (it's free!)
3. Verify your email
4. Go to "API keys" section
5. Copy your API key

⚠️ **Note**: API key takes 10-15 minutes to activate after creation.

### Step 2: Deploy (1 minute)

**Option A: Railway (Easiest)**
1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select this repository
5. Add variable: `OPENWEATHER_API_KEY` = [your key]
6. Click "Deploy"
7. Generate domain in Settings
8. Done! Copy your URL

**Option B: Render**
1. Go to https://render.com
2. New → Web Service
3. Connect repository
4. Build: `pip install -r requirements.txt`
5. Start: `gunicorn app:app`
6. Add environment variable: `OPENWEATHER_API_KEY`
7. Create Web Service
8. Copy your .onrender.com URL

### Step 3: Submit

1. Copy your deployment URL
2. Open `my_dark_sky_url.txt`
3. Paste URL on first line
4. Save file

## Local Development

Want to test locally first?

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file
cp .env.example .env

# 3. Edit .env and add your API key
OPENWEATHER_API_KEY=your_key_here

# 4. Run the app
python app.py

# 5. Open browser
http://localhost:5000
```

Or use the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

## File Structure

```
mydarksky/
├── app.py              # Flask backend
├── templates/
│   └── index.html      # Frontend app
├── requirements.txt    # Dependencies
├── .env.example        # Environment template
├── README.md           # Documentation
├── DEPLOYMENT.md       # Deployment guide
└── ARCHITECTURE.md     # Technical details
```

## Features

### 🔍 Search
Type any city name: "New York", "London", "Tokyo"

### 📍 Geolocation
Click the 📍 button to use your current location

### 📅 Forecast
See 8-day forecast with temperature ranges and conditions

### ⏳ Time Machine
Pick any date to see historical weather (requires paid API plan)

### 💾 Cache
Automatic 5-minute cache reduces API calls and speeds up responses

## Troubleshooting

**"API key invalid"**
- Wait 10-15 minutes after creating API key
- Check you copied the key correctly
- Verify it's set in environment variables

**"Location not found"**
- Try being more specific: "Paris, France" instead of "Paris"
- Check your internet connection
- Verify geocoding is working

**"Time Machine not working"**
- Historical data requires paid OpenWeather plan ($40/month)
- Free tier only supports current + 5-day forecast
- Consider removing this feature or using mock data

**App is slow**
- First request on free tier has "cold start"
- Subsequent requests use cache (much faster!)
- Consider upgrading hosting plan

## API Limits (Free Tier)

- 1,000 API calls per day
- 60 calls per minute
- Current weather: ✅ Included
- 5-day forecast: ✅ Included
- Historical data: ❌ Paid only ($40/month)

Our cache system helps you stay within limits!

## Next Steps

1. **Deploy** using Railway or Render
2. **Test** all features work correctly
3. **Copy URL** to `my_dark_sky_url.txt`
4. **Submit** your project
5. **Share** with friends! 🎉

## Support

- **API Issues**: https://openweathermap.org/faq
- **Deployment**: See DEPLOYMENT.md
- **Architecture**: See ARCHITECTURE.md

## Made With

- Python & Flask
- Tailwind CSS
- OpenWeather API
- Love for beautiful weather apps ❤️

---

**Note**: This project is for educational purposes. The original Dark Sky was created by The Dark Sky Company and acquired by Apple in 2020.
