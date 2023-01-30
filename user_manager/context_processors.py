from .models import Weather

def weather_context(request):
    context_data = dict()
    try:
        context_data['current_weather'] = f'{int(Weather.objects.get(pk=1).temp)} F'
    except:
        context_data['current_weather'] = "N/A"
    return context_data