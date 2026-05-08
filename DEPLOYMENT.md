# Quick Deployment Guide

## Fastest Options (Recommended)

### 1. Render (Easiest - Free Tier Available)

**Steps:**
1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub/GitLab repository (or deploy from GitHub directly)
4. Configure:
   - **Name**: mydarksky (or your choice)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Add Environment Variable:
   - Key: `OPENWEATHER_API_KEY`
   - Value: [Your OpenWeather API key]
6. Click "Create Web Service"
7. Wait 2-3 minutes for deployment
8. Your URL will be: `https://mydarksky.onrender.com`

**Note**: Free tier may spin down after inactivity. First request might be slow.

---

### 2. Railway (Very Easy - Free Tier Available)

**Steps:**
1. Go to [railway.app](https://railway.app) and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-detects Python/Flask
5. Go to "Variables" tab
6. Add: `OPENWEATHER_API_KEY` = [Your API key]
7. Click "Deploy"
8. Go to "Settings" → "Generate Domain"
9. Your URL will be: `https://mydarksky.up.railway.app`

---

### 3. Heroku (Classic Option - Paid)

**Steps:**
1. Install Heroku CLI: `brew install heroku` (Mac) or download from heroku.com
2. Login: `heroku login`
3. Create app: `heroku create mydarksky`
4. Set API key: `heroku config:set OPENWEATHER_API_KEY=your_api_key`
5. Deploy: `git push heroku main`
6. Open: `heroku open`

Your URL: `https://mydarksky.herokuapp.com`

---

### 4. Vercel (For Serverless)

**Steps:**
1. Install Vercel CLI: `npm i -g vercel`
2. In project directory: `vercel login`
3. Deploy: `vercel --prod`
4. When prompted, select defaults
5. Go to Vercel dashboard → Project → Settings → Environment Variables
6. Add: `OPENWEATHER_API_KEY` = [Your API key]
7. Redeploy: `vercel --prod`

Your URL: `https://mydarksky.vercel.app`

---

## Getting OpenWeather API Key

1. Go to [openweathermap.org](https://openweathermap.org/api)
2. Sign up for free account
3. Go to API Keys section
4. Copy your API key
5. **Important**: Free tier limits:
   - 1,000 calls/day
   - 60 calls/minute
   - Current weather & 5-day forecast included
   - Historical data requires paid plan (for Time Machine feature)

---

## Testing Locally First

Before deployment, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "OPENWEATHER_API_KEY=your_key_here" > .env

# Run app
python app.py

# Open browser
open http://localhost:5000
```

---

## Troubleshooting

**Problem**: "API key invalid"
- Check your API key is correct in environment variables
- Wait 10-15 minutes after creating new OpenWeather API key (activation time)

**Problem**: "Time Machine not working"
- Historical data requires OpenWeather paid plan ($40/month)
- Free tier only supports current weather + 5-day forecast
- Consider removing Time Machine feature or using mock data

**Problem**: "App is slow"
- Free tiers may have cold starts
- Cache is working - second request should be faster
- Consider upgrading to paid tier for better performance

**Problem**: "Location search not working"
- Check internet connection
- Verify geocoding API is included in your OpenWeather plan (it is in free tier)

---

## After Deployment

1. Test these features:
   - Search for different cities
   - Use "locate me" button
   - Check forecast accuracy
   - Try Time Machine (if you have paid API)

2. Copy your deployment URL to `my_dark_sky_url.txt`

3. Share and enjoy! 🌤️
