import time
import requests

from render.models import Imovel


def fetch_property_data(url, headers, payload):
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erro ao fazer a requisição: {e}")
        return None

def parse_property_data(dados):
    properties = []
    for item in dados['data']:
        try:
            property_data = {
                "Imobiliaria": "Pedrão",
                "Tipo": item.get("finalidade_im", "N/A"),
                "Bairro": item.get("bairro_im", "N/A"),
                "Valor": item.get("valor", "N/A")
            }
            properties.append(property_data)
        except AttributeError as e:
            print(f"Erro ao extrair dados do imóvel: {e}")
    return properties

def save_property_data(properties):
    try:
        imovel = Imovel(
            imobiliaria=property["Imobiliaria"],
            tipo=property["Tipo"],
            bairro=property["Bairro"],
            valor=property["Valor"]
        )
        imovel.save()
        print(f"Imóvel salvo: {imovel}")
    except Exception as e:
        print(f"Erro ao salvar o imóvel: {e}")

def main():
    url = "https://waysoft.net.br/apiapp/API-IMOB/api/buscar-im/9291f67888d4058261e3d36ff6b12ad5"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Length": "266",
        "Content-Type": "application/json",
        "Origin": "https://www.pedraoimoveis.com.br",
        "Priority": "u=1, i",
        "Referer": "https://www.pedraoimoveis.com.br/",
        "Sec-Ch-Ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }

    result = []
    PAGE_INDEX = 0
    has_data = True

    while has_data:
        payload = {
            "FOR_SALE_OR_LOCATION": 1,
            "TYPE": "Todos",
            "CITY": "SANTA RITA DO SAPUCAÍ",
            "NEIGHBORHOOD": "Todos",
            "QUARTO": "Todos",
            "GARAGEM": "Todos",
            "MIN_VALUE_FOR_SALE": None,
            "MAX_VALUE_FOR_SALE": None,
            "MIN_VALUE_LOCATION": "Todos",
            "MAX_VALUE_LOCATION": "Todos",
            "LIMIT": 0,
            "PAGE_INDEX": PAGE_INDEX
        }

        dados = fetch_property_data(url, headers, payload)
        if dados:
            TOTAL_PAGE = int(dados['totalItens']) // 12

            if TOTAL_PAGE > PAGE_INDEX:
                result.extend(parse_property_data(dados))
                PAGE_INDEX += 1
                time.sleep(10)  # Aguardar 10 segundos antes da próxima requisição
            else:
                has_data = False
        else:
            has_data = False

    save_property_data(result)

if __name__ == "__main__":
    main()