import requests
import urllib.parse as urlparse

country = "Paris"
key = "6ba5cf7b"
urlplace = 'https://nominatim.openstreetmap.org/search/'+ urlparse.quote(country) +'?format=json'
responseplace = requests.get(urlplace).json()
weather = requests.get(f"https://api.hgbrasil.com/weather?key={key}&lat={(responseplace[0]['lat'])}&lon={(responseplace[0]['lon'])}&user_ip=remote")
weatherresp = weather.json()

print(type(weatherresp))
print (weatherresp)