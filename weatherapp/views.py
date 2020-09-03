from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from .models import City
from .forms import CityForm

def index(request):
	url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=8e2d8db08786470980d247fc1609ee35'

	err_msg = ''

	if request.method == 'POST':
		form = CityForm(request.POST)
		if form.is_valid():
			new_city = form.cleaned_data['name']
			existing_city_count = City.objects.filter(name=new_city).count()
			if existing_city_count == 0:
				form.save()
			else:
				err_msg = 'City already exists in the Database!'

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

	print(weather_data)

	context = {
		'weather_data' : weather_data,




		'form' : form
	}

	return render(request, "weatherapp/weather.html", context)


def delete_city(request, city_name):
	City.objects.get(name = city_name).delete()

	return redirect('home')