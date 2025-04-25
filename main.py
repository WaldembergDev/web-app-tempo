import requests
from dotenv import load_dotenv
import os
import streamlit as st

# carregando o ambiente virtual
load_dotenv(r'.venv/.env')

# obtendo o token
TOKEN = os.getenv('TOKEN')


def obter_latitude_longitude(cidade: str):
    # obtendo a latitude e longitude
    url_latitude_longitude = 'http://api.openweathermap.org/geo/1.0/direct'

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
    url = 'https://api.openweathermap.org/data/2.5/weather'

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
    st.header(body='Web App Tempo', divider=True)
    st.write(
        'Acesse a OpenWeather clicando '
        '[aqui](https://openweathermap.org/current).'
        )
    local = st.text_input(label='Busque uma cidade: ')
    if not local:
        st.stop()
    dados_latitude_longitude = obter_latitude_longitude(local)
    if not dados_latitude_longitude:
        st.warning(
            f'A cidade {local} não foi encontrada!'
            'Procure por outra cidade.'
            )
    latitude = dados_latitude_longitude[0]
    Longitude = dados_latitude_longitude[1]
    dados_tempo = obter_previsao_tempo(latitude=latitude, logintude=Longitude)
    # salvando os dados em uma váriavel
    tempo_atual = dados_tempo['weather'][0].get('description')
    temperatura_atual = dados_tempo['main'].get('temp')
    temperatura_maxima = dados_tempo['main'].get('temp_max')
    temperatura_minima = dados_tempo['main'].get('temp_min')
    sensacao_termica = dados_tempo['main'].get('feels_like')
    umidade = dados_tempo['main'].get('humidity')
    cortura_nuvens = dados_tempo['clouds'].get('all')
    # criando uma visualização no streamlit
    st.metric(label='Tempo atual', value=tempo_atual)
    # dividindo a aplicação em duas colunas
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label='Temperatura atual (ºC)', value=temperatura_atual)
        st.metric(label='Temperatura máxima (ºC)', value=temperatura_maxima)
        st.metric(label='Temperatura mínima (ºC)', value=temperatura_minima)
    with col2:
        st.metric(label='Sensação térmica (ºC)', value=sensacao_termica)
        st.metric(label='Humidade (%)', value=umidade)
        st.metric(label='Cobertura de nuvens (%)', value=cortura_nuvens)


if __name__ == '__main__':
    main()
