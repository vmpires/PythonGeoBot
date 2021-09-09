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
        key = os.environ['hgbrasilkey']
        urlplace = 'https://nominatim.openstreetmap.org/search/'+ urlparse.quote(country) +'?format=json'
        responseplace = requests.get(urlplace).json()
        weather = requests.get(f"https://api.hgbrasil.com/weather?key={key}&lat={(responseplace[0]['lat'])}&lon={(responseplace[0]['lon'])}&user_ip=remote")
        weatherresp = weather.json()
        return (f"Descrição do tempo: {weatherresp['description']}")

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
