import requests
from pprint import pprint
from dotenv import load_dotenv
import os

# carregando o ambiente virtual
load_dotenv(r'.venv/.env')

# obtendo o token
TOKEN = os.getenv('TOKEN')


def obter_latitude_longitude(cidade: str):
    # obtendo a latitude e longitude
    url_latitude_longitude = f'http://api.openweathermap.org/geo/1.0/direct'

    # passando os parâmetros obrigatórios
    params = {
        'q': cidade,
        'appid': TOKEN
    }

    response = requests.get(url_latitude_longitude, params=params)

    try:
        response.raise_for_status()
        if response.json():
            latitude = response.json()[0].get('lat')
            longitude = response.json()[0].get('lon')
            return latitude, longitude
        else:
            return None
    except requests.HTTPError as e:
        print(f'Erro ao realizar a requisição: {e}')
        return None


def obter_previsao_tempo(latitude, logintude):
    url = f'https://api.openweathermap.org/data/2.5/weather'

    params = {
        'lat': latitude,
        'lon': logintude,
        'appid': TOKEN,
        'units': 'metric',
        'lang': 'pt_br'
    }

    response = requests.get(url, params=params)

    try:
        response.raise_for_status()
        return response.json() if response.json() else None
    except requests.HTTPError as e:
        print(f'Erro ao realizar a requisição: {e}')

def main():
    pass


if __name__ == '__main__':
    resultado = obter_latitude_longitude('Duque de caxias')

    previsao = obter_previsao_tempo(resultado[0], resultado[1])

    pprint(previsao)