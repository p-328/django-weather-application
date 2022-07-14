from django.http import HttpRequest
from django.shortcuts import redirect, render
from .models import City
from django.urls import reverse
from django.contrib import messages
import requests
from geopy.geocoders import Nominatim
from .forms import CityForm

locator = Nominatim(user_agent='locator')


def get_data_of_city(city: str, country_or_state: str):
    weather_data_raw = requests.get(
        f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city},{country_or_state}?key=CC7Q5GYJQEFFCEPWHEDWRUS47")
    weather_data_dict = weather_data_raw.json()['days']
    weather_data_filter = [
        (day['datetime'],
         day['tempmax'],
         day['tempmin'],
         day['temp'],
         day['humidity']) for day in weather_data_dict]
    return (
        weather_data_raw.json()['description'],
        weather_data_filter,
        weather_data_raw.json()['resolvedAddress'])

# Create your views here.


def index(request: HttpRequest):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CityForm(request.POST)
            if form.is_valid():
                existing_cities = City.objects.filter(
                    city_name=form.cleaned_data['city'], user=request.user)
                if len(existing_cities) > 0:
                    messages.error(request, 'City already exists!')
                    return redirect(reverse('cities-page'))
                location = locator.geocode(
                    f"{form.cleaned_data['city']},{form.cleaned_data['country_or_state']}")
                if location is None:
                    messages.error(request, 'That location does not exist!')
                    return redirect(reverse('cities-page'))
                list(messages.get_messages(request))
                new_city = City(
                    city_name=form.cleaned_data['city'],
                    country_or_state=form.cleaned_data['country_or_state'],
                    user=request.user)
                new_city.save()
                return redirect(reverse('cities-page'))
        else:
            form = CityForm()
        cities = City.objects.filter(user=request.user)
        ctx = {
            'username': request.user.username,
            'cities': cities,
            'form': form
        }
        return render(request, 'city_page.html', ctx)
    else:
        return redirect(reverse('login-screen'))


def get_city_by_id(request: HttpRequest, id: int):
    if request.user.is_authenticated:
        cities = City.objects.filter(user=request.user, id=id)
        if len(cities) == 0:
            messages.error(request=request, message='City not found!')
            return redirect(reverse('cities-page'))
        if request.method == "DELETE":
            cities.delete()
            messages.warning(request, 'Deleted city.')
            return redirect(reverse('cities-page'))
        city = cities[0]
        description, data, expanded_name = get_data_of_city(
            city=city.city_name, country_or_state=city.country_or_state)
        data_ctx = {
            'weather_data': data,
            'description': description,
            'expanded_name': expanded_name
        }
        return render(
            request=request,
            template_name='detail.html',
            context=data_ctx)
    else:
        return redirect(reverse('login-screen'))
