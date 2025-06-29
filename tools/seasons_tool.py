from datetime import date
from tools.weather_tool import get_location_by_ip  # reaproveita seu código!

def inferir_estacao_por_geolocalizacao(_input: str = None) -> str:
    """
    Checks the season based on geolocation
    """
   
    data = date.today()

    try:
        local = get_location_by_ip()
        if not local:
            return "❌ Localização não identificada. Não foi possível inferir a estação do ano."

        latitude = local["latitude"]
        cidade = local["cidade"]
        hemisferio = "sul" if latitude < 0 else "norte"

        dia = data.day
        mes = data.month

        if hemisferio == "sul":
            if (mes == 12 and dia >= 21) or mes in [1, 2] or (mes == 3 and dia < 20):
                estacao = "verão"
            elif (mes == 3 and dia >= 20) or mes in [4, 5] or (mes == 6 and dia < 21):
                estacao = "outono"
            elif (mes == 6 and dia >= 21) or mes in [7, 8] or (mes == 9 and dia < 23):
                estacao = "inverno"
            else:
                estacao = "primavera"
        else:  # hemisfério norte
            if (mes == 12 and dia >= 21) or mes in [1, 2] or (mes == 3 and dia < 20):
                estacao = "inverno"
            elif (mes == 3 and dia >= 20) or mes in [4, 5] or (mes == 6 and dia < 21):
                estacao = "primavera"
            elif (mes == 6 and dia >= 21) or mes in [7, 8] or (mes == 9 and dia < 23):
                estacao = "verão"
            else:
                estacao = "outono"

        return (
            f"📍 Local detectado: {cidade} ({'Hemisfério Sul' if hemisferio == 'sul' else 'Hemisfério Norte'})\n"
            f"🗓️ Estação atual: {estacao.capitalize()}"
        )

    except Exception as e:
        return f"❌ Erro ao inferir estação: {e}"
