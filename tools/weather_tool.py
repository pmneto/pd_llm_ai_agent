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

        atual_temp = atual.get("temperature", "indisponível")
        vento = atual.get("windspeed", "indisponível")

        resumo_atual = (
            f"📍 Clima atual na sua região:\n"
            f"- Temperatura agora: {atual_temp}°C\n"
            f"- Velocidade do vento: {vento} km/h\n"
        )

        # Previsão para os próximos 3 dias (incluindo hoje)
        previsoes = "\n🗓️ Previsão para os próximos dias:\n"
        dias_para_prever = min(3, len(diario["time"]))  # segurança

        for i in range(idx_hoje, idx_hoje + dias_para_prever):
            data_dia = datetime.strptime(diario["time"][i], "%Y-%m-%d")
            dia_semana = data_dia.strftime("%A").capitalize()
            max_temp = diario["temperature_2m_max"][i]
            min_temp = diario["temperature_2m_min"][i]
            chuva = diario["precipitation_sum"][i]

            previsoes += (
                f"- {dia_semana} ({data_dia.strftime('%d/%m')}): "
                f"máx {max_temp}°C, mín {min_temp}°C, chuva esperada: {chuva} mm\n"
            )

        return resumo_atual + previsoes

    except Exception as e:
        print(f"Erro ao obter clima: {e}")
        return "❌ Não foi possível obter os dados climáticos no momento."

def consultar_clima(_input=None):
    loc = get_location_by_ip()
    if loc:
        return get_weather_forecast(loc["latitude"], loc["longitude"])
    return "❌ Localização não identificada."
