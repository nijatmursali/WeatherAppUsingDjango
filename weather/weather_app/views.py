from django.shortcuts import render
import requests
# Create your views here.
from .models import City
from .forms import CityForm

def index(request):

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=80efc66af0e25c9f30cab86a90c87618'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()
    weather_data = []
    
    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'weather/weather.html', context)