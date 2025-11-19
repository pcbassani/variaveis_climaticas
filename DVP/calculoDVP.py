import requests
import math

def calcular_vpd(temperatura, umidade_relativa):
    """
    Calcula o Déficit de Pressão de Vapor (VPD) em kPa.

    Args:
        temperatura (float): Temperatura do ar em graus Celsius.
        umidade_relativa (float): Umidade relativa em porcentagem.

    Returns:
        float: O valor do VPD em quiloPascais (kPa).
    """
    # equação de Tetens
    svp = 0.61078 * math.exp((17.27 * temperatura) / (temperatura + 237.3))
    avp = svp * (umidade_relativa / 100)
    vpd = svp - avp

    return vpd

latitude = -23.55
longitude = -46.63

url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m"

try:
    response = requests.get(url )
    response.raise_for_status()  
    data = response.json()

    temperatura_atual = data['current']['temperature_2m']
    umidade_relativa_atual = data['current']['relative_humidity_2m']

    vpd_calculado = calcular_vpd(temperatura_atual, umidade_relativa_atual)

    print(f"Dados atuais para a localização (Lat: {latitude}, Lon: {longitude}):")
    print(f"  - Temperatura: {temperatura_atual}°C")
    print(f"  - Umidade Relativa: {umidade_relativa_atual}%")
    print("---")
    print(f"O Déficit de Pressão de Vapor (VPD) é: {vpd_calculado:.2f} kPa")

except requests.exceptions.RequestException as e:
    print(f"Erro ao buscar dados do tempo: {e}")
except KeyError:
    print("Não foi possível processar a resposta da API. A estrutura pode ter mudado.")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")

