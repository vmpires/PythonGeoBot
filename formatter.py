import requests
import os
import urllib.parse as urlparse
import json
import wikipedia as wiki

class Formatter:

    def __init__(self):
        self.key = os.environ['openweatherkey']
    
    def kelvintocelsius(value):
        return (value-273)

    def get_flag(flag):
        f = open("countries.json")
        countries = json.load(f)
        for item in countries:
            if item["code"] == flag:
                return(f"{item['name']} {item['emoji']}")

    def get_weather(self, place):
        
        if isinstance(place, str):
            urlplace = 'https://nominatim.openstreetmap.org/search/'+ urlparse.quote(place) +'?format=json'
            responseplace = requests.get(urlplace).json()
            weather = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={(responseplace[0]['lat'])}&lon={(responseplace[0]['lon'])}&appid={self.key}")
            weatherresp = weather.json()
        elif isinstance(place, list):
            weather = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={place[0]}&lon={place[1]}&appid={self.key}")
            weatherresp = weather.json()

        return (f"Place: {weatherresp['name']}\n\
Country: {self.get_flag(weatherresp['sys']['country'])}\n\
Description: {weatherresp['weather'][0]['description']}\n\
Current Temperature: {self.kelvintocelsius(weatherresp['main']['temp']):.0f}° Celsius\n\
Feeling like: {self.kelvintocelsius(weatherresp['main']['feels_like']):.0f}° Celsius\n\
Max Temperature: {self.kelvintocelsius(weatherresp['main']['temp_max']):.0f}° Celsius\n\
Min Temperature: {self.kelvintocelsius(weatherresp['main']['temp_min']):.0f}° Celsius\n\
Humidity: {weatherresp['main']['humidity']}%\n\
Wind Speed: {weatherresp['wind']['speed']} m/s\n\
Atmospheric Pressure: {weatherresp['main']['pressure']} hPa")

    
    def get_placeinfo(self, place):
        urlplace = 'https://nominatim.openstreetmap.org/search/'+ urlparse.quote(place) +'?format=json'
        responseplace = requests.get(urlplace).json()
        weather = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={(responseplace[0]['lat'])}&lon={(responseplace[0]['lon'])}&appid={self.key}")
        weatherresp = weather.json()
        flag = Formatter.get_flag(weatherresp['sys']['country'])
        
        try:
            wikisum = wiki.summary(place)
            latlonresult = wiki.geosearch(responseplace[0]['lat'], responseplace[0]['lon'], title=None, results=5, radius=3000)
        except:
            latlonresult = wiki.geosearch(responseplace[0]['lat'], responseplace[0]['lon'], title=None, results=5, radius=3000)
            wikisum = wiki.summary(latlonresult[0])
        
        relplaces = ", ".join(latlonresult)
        endresult = f"{wikisum}\n\nCountry: {flag}\n\nRelated places: {relplaces}"
        return (endresult)
