import requests
import os
import urllib.parse as urlparse
import json

class Formatter:

    def format_amount(amount):

        if amount < 10**6:
            # Thousands
            return f"{'{:,}'.format(amount)}".replace(',', '.')
        elif amount < 10**9:
            # Millions
            return f"{'{:,}'.format(amount)}".replace(',', '.')
        elif amount < 10**12:
                # Billions
            return f"{'{:,}'.format(amount)}".replace(',', '.')
        else:
            # Trillions
            return f"{'{:,}'.format(amount)}".replace(',', '.')

    def get_weather(country):
        key = os.environ['openweatherkey']
        urlplace = 'https://nominatim.openstreetmap.org/search/'+ urlparse.quote(country) +'?format=json'
        responseplace = requests.get(urlplace).json()
        weather = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={(responseplace[0]['lat'])}&lon={(responseplace[0]['lon'])}&appid={key}")
        weatherresp = weather.json()
        celsiustemp = (weatherresp['main']['temp'] - 273) # Kelvin to Celsius
        celsiusfeelslike = (weatherresp['main']['feels_like'] - 273) # Kelvin to Celsius
        celsiusmax = (weatherresp['main']['temp_max'] - 273)
        celsiusmin = (weatherresp['main']['temp_min'] - 273)
        flag = Formatter.get_flag(weatherresp['sys']['country'])
        return (f"City: {weatherresp['name']}\n\
Country: {flag}\n\
Description: {weatherresp['weather'][0]['description']}\n\
Current Temperature: {celsiustemp:.0f}° Celsius\n\
Feeling like: {celsiusfeelslike:.0f}° Celsius\n\
Max Temperature: {celsiusmax:.0f}° Celsius\n\
Min Temperature: {celsiusmin:.0f}° Celsius\n\
Humidity: {weatherresp['main']['humidity']}%\n\
Wind Speed: {weatherresp['wind']['speed']} m/s\n\
Atmospheric Pressure: {weatherresp['main']['pressure']} hPa")

    def get_flag(flag):
        f = open("countries.json")
        countries = json.load(f)
        for item in countries:
            if item["code"] == flag:
                return(f"{item['name']} {item['emoji']}")
