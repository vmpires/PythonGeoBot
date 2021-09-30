import requests
import urllib.parse as urlparse
from formatter import Formatter as f

key = "393d1210275a761bd071334eb214527b"
def get_weather(place):
    
    if isinstance(place, str):
        urlplace = 'https://nominatim.openstreetmap.org/search/'+ urlparse.quote(place) +'?format=json'
        responseplace = requests.get(urlplace).json()
        weather = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={(responseplace[0]['lat'])}&lon={(responseplace[0]['lon'])}&appid={key}")
        weatherresp = weather.json()
    elif isinstance(place, list):
        weather = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={place[0]}&lon={place[1]}&appid={key}")
        weatherresp = weather.json()

    return (f"Place: {weatherresp['name']}\n\
Country: {f.get_flag(weatherresp['sys']['country'])}\n\
Description: {weatherresp['weather'][0]['description']}\n\
Current Temperature: {f.kelvintocelsius(weatherresp['main']['temp']):.0f}° Celsius\n\
Feeling like: {f.kelvintocelsius(weatherresp['main']['feels_like']):.0f}° Celsius\n\
Max Temperature: {f.kelvintocelsius(weatherresp['main']['temp_max']):.0f}° Celsius\n\
Min Temperature: {f.kelvintocelsius(weatherresp['main']['temp_min']):.0f}° Celsius\n\
Humidity: {weatherresp['main']['humidity']}%\n\
Wind Speed: {weatherresp['wind']['speed']} m/s\n\
Atmospheric Pressure: {weatherresp['main']['pressure']} hPa")

if __name__ == "__main__":

    latlon = [-23.6596055,-46.5381533]
    print(get_weather("Rio de Janeiro"))
    print(get_weather(latlon))