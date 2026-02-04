# 🌤️ SkyCast Weather Dashboard

A high-end, one-sight weather intelligence dashboard built with **Django** and **Tailwind CSS**. Designed for a modern, zero-scroll user experience using Glassmorphism aesthetics.

## ✨ Key Features
- **One-Sight UI:** A compact, responsive dashboard that fits perfectly in the viewport without scrolling.
- **AI-Powered Insights:** Custom logic that analyzes weather data to provide daily advice (e.g., "Stay hydrated" or "Carry an umbrella").
- **Geolocation Support:** Integrated browser Geolocation API to fetch weather data for your current coordinates instantly.
- **5-Day Extended Forecast:** Detailed weather outlook using data from OpenWeatherMap.
- **Performance Optimized:** Server-side caching implemented to reduce API overhead and improve load times.
- **Professional Testing:** Comprehensive test suite with mocking for API reliability.

## 🛠️ Tech Stack
- **Backend:** Python 3.12, Django 6.0
- **Frontend:** Tailwind CSS (Glassmorphism design)
- **API:** OpenWeatherMap API
- **Tools:** Python-Dotenv (Environment Variables), Gunicorn (Production Server), WhiteNoise (Static Files)

## 🚀 Local Setup
1. **Clone the repo:** `git clone <your-repo-link>`
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Configure Environment:** Create a `.env` file and add your `WEATHER_API_KEY`.
4. **Run Server:** `python manage.py runserver`

## ☁️ Deployment
This project is configured for a one-click deployment on **Render** using the provided `build.sh` script.