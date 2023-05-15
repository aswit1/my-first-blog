from django.conf import settings
import requests
from django.shortcuts import redirect
from celery import shared_task
from user_manager.models import Weather

@shared_task
def get_weather():
    print("starting task**************************************************************************")
    api_key = settings.WEATHER_API_KEY
    weather_latitude = settings.WEATHER_LATITUDE
    weather_longitude = settings.WEATHER_LONGITUDE
    api_call = f'https://api.openweathermap.org/data/2.5/weather?lat={weather_latitude}&lon={weather_longitude}&appid={api_key}&units=imperial'
    response = requests.get(api_call)
    json_data = response.json()
    print(json_data['main']['temp'])
    weather_data, created = Weather.objects.get_or_create(pk=1)
    weather_data.temp = json_data['main']['temp']
    weather_data.save()
    return 'hello'
