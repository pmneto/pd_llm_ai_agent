import requests
from datetime import datetime

def get_location_by_ip():
    try:
        res = requests.get("https://ipinfo.io/json")
        data = res.json()
        lat, lon = map(float, data["loc"].split(","))
        cidade = data.get("city", "")
        return {"latitude": lat, "longitude": lon, "cidade": cidade}
    except Exception as e:
        print(f"Erro ao obter localização: {e}")
        return None

def get_weather_forecast(latitude, longitude):
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}&longitude={longitude}&current_weather=true&"
            f"daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=America/Sao_Paulo"
        )
        res = requests.get(url)
        data = res.json()

        atual = data.get("current_weather", {})
        diario = data.get("daily", {})

        hoje = datetime.today().strftime("%Y-%m-%d")
        idx_hoje = diario["time"].index(hoje) if hoje in diario["time"] else 0

        max_temp = diario["temperature_2m_max"][idx_hoje]
        min_temp = diario["temperature_2m_min"][idx_hoje]
        chuva = diario["precipitation_sum"][idx_hoje]
        atual_temp = atual.get("temperature", "indisponível")
        vento = atual.get("windspeed", "indisponível")

        resumo = (
            f"📍 Clima atual na sua região:\n"
            f"- Temperatura agora: {atual_temp}°C\n"
            f"- Máxima do dia: {max_temp}°C | Mínima: {min_temp}°C\n"
            f"- Precipitação esperada: {chuva} mm\n"
            f"- Velocidade do vento: {vento} km/h"
        )
        return resumo

    except Exception as e:
        print(f"Erro ao obter clima: {e}")
        return "❌ Não foi possível obter os dados climáticos no momento."

def consultar_clima(_input=None):
    loc = get_location_by_ip()
    if loc:
        return get_weather_forecast(loc["latitude"], loc["longitude"])
    return "❌ Localização não identificada."
