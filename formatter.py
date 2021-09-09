import requests
import os
import urllib.parse as urlparse

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
        return (f"Place: {weatherresp['name']}\n\
Description: {weatherresp['weather'][0]['description']}\n\
Temperature: {weatherresp['main']['temp']}º Fahrenheit.\n\
Feeling like: {weatherresp['main']['feels_like']}º Fahrenheit.\n\
Humidity: {weatherresp['main']['humidity']}%.")

    def get_uf(uf):
        urluf = (f"https://covid19-brazil-api.now.sh/api/report/v1/brazil/uf/{uf}")
        responseuf = requests.get(urluf)
        contentuf = responseuf.json()
        return (f"Estado: {contentuf['state']}\nCasos: {Formatter.format_amount(contentuf['cases'])}\nMortes: {Formatter.format_amount(contentuf['deaths'])}")

    def get_country(pais):
        urlpais = (f"https://covid19-brazil-api.now.sh/api/report/v1/countries")
        responsepais = requests.get(urlpais)
        contentpais = responsepais.json()
        if pais[0].islower():
            pais = pais.capitalize()
        for item in contentpais['data']:
                if pais in item['country']:
                    return (f"País: {item['country']}\nCasos confirmados: {Formatter.format_amount(item['confirmed'])}\nMortes: {Formatter.format_amount(item['deaths'])}")
        return ("País não encontrado, tente novamente.")
