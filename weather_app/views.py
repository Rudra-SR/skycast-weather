import os
import requests
from django.shortcuts import render
from django.core.cache import cache
from dotenv import load_dotenv

load_dotenv()

def get_recommendations(temp, desc):
    """Algorithm for weather-based advice."""
    desc = desc.lower()
    if temp > 30: return "It's scorching! Stay hydrated."
    elif temp < 15: return "Chilly! Grab a warm jacket."
    elif "rain" in desc or "drizzle" in desc: return "Rain expected. Carry an umbrella!"
    else: return "Pleasant weather today!"

def index(request):
    api_key = os.getenv("WEATHER_API_KEY")
    weather_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + api_key
    coord_url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid=' + api_key
    forecast_url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=' + api_key
    forecast_coord_url = 'http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&units=metric&appid=' + api_key
    
    weather_data, forecast_list, error_msg = None, [], None
    
    # UPDATED: Set Bengaluru as the default starting city
    search_city = "Bangalore" 
    
    lat, lon = None, None

    if request.method == 'POST':
        city_input = request.POST.get('city', '').strip()
        lat, lon = request.POST.get('lat'), request.POST.get('lon')
        if city_input:
            search_city = city_input

    # Caching check for optimization
    cache_key = f"weather_{search_city.lower()}" if not lat else f"weather_{lat}_{lon}"
    cached_result = cache.get(cache_key)

    if cached_result:
        weather_data, forecast_list = cached_result['current'], cached_result['forecast']
    else:
        if lat and lon:
            current_res = requests.get(coord_url.format(lat, lon)).json()
            fore_res = requests.get(forecast_coord_url.format(lat, lon)).json()
        else:
            current_res = requests.get(weather_url.format(search_city)).json()
            fore_res = requests.get(forecast_url.format(search_city)).json()

        if current_res.get('cod') == 200:
            temp, desc = current_res['main']['temp'], current_res['weather'][0]['description']
            weather_data = {
                'city': current_res.get('name'),
                'temperature': temp,
                'description': desc,
                'icon': current_res['weather'][0]['icon'],
                'humidity': current_res['main']['humidity'],
                'wind_speed': current_res['wind']['speed'],
                'advice': get_recommendations(temp, desc),
            }
            if fore_res.get('cod') == "200":
                forecast_list = [{'temp': i['main']['temp'], 'icon': i['weather'][0]['icon'], 'day': i['dt_txt'][8:10]} for i in fore_res['list'][::8]]
            cache.set(cache_key, {'current': weather_data, 'forecast': forecast_list}, 900)
        else:
            api_error_code = current_res.get('cod')
            if api_error_code == "404" or api_error_code == 404:
                error_msg = f"We couldn't find '{search_city}'. Please check the spelling or try searching for a larger nearby city."
            elif api_error_code == "401" or api_error_code == 401:
                error_msg = "System Error: The Weather API key is invalid. Please contact the administrator."
            elif api_error_code == "429" or api_error_code == 429:
                error_msg = "We're receiving too many requests right now. Please wait a moment and try again."
            else:
                error_msg = "An unexpected error occurred while fetching the weather. Please try again later."

    return render(request, 'weather_app/index.html', {
        'weather_data': weather_data, 
        'forecast_list': forecast_list, 
        'error_msg': error_msg
    })