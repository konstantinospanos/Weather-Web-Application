import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

def index(request):
    
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=9c33efad3575ee964fd7556466434a5c'
    
    err_msg = ''
    
    if request.method == 'POST': # press submit Add City
        form = CityForm(request.POST)
        
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            # prevent duplicate cities
            if existing_city_count == 0: 
                r = requests.get(url.format(new_city)).json() # get url city
                if r['cod'] == 200: 
                    err_msg = 'City/Country Create in databases!'
                    form.save()
                else:
                    err_msg = 'City/Country does not exist in the world!'
            else:
                err_msg = 'City/Country already exists in the database!'
                
    
    form = CityForm()
    
    cities = City.objects.all()
    
    weather_data = []
    
    for city in cities: 
    
        r = requests.get(url.format(city)).json() # get url city
        
        city_weather = {
            
        'city' : city.name,
        'temperature' : r['main']['temp'],
        'description' : r['weather'][0]['description'],
        'icon' : r['weather'][0]['icon']
        }
        
        weather_data.append(city_weather)
        
    context = {
        'weather_data' : weather_data, 
        'form' : form ,
        'err_msg': err_msg
    }
      
    return render(request, 'weather/weather.html', context) #contact dict-display html


def delete_city(request, city_name):
    
    City.objects.get(name=city_name).delete()
    return redirect('weather')











 
