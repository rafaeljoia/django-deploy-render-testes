from bs4 import BeautifulSoup
import httpx

from models import Imovel



def fetch_property_data(url, headers):
    try:
        response = httpx.get(url, headers=headers, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    except httpx.RequestError as e:
        print(f"Erro ao fazer a requisição: {e}")
        return None
    except Exception as e:
        print(f"Erro ao analisar o conteúdo HTML: {e}")
        return None

def parse_property_data(soup):
    properties = []
    divs_imoveis = soup.find_all("div", class_="single-featured-property mb-50 wow fadeInUp")
    for div_imovel in divs_imoveis:
        try:
            valor_div = div_imovel.find("div", class_="list-price").find("p").find("span").text.strip()
            tipo_div = div_imovel.find("div", class_="property-content").find("h5").text.strip()
            bairro_div = div_imovel.find("div", class_="property-content").find("p", class_="location").text.strip().replace("Bairro", "").strip()
            property_data = {
                "Valor": valor_div,
                "Tipo": tipo_div,
                "Bairro": bairro_div,
                "Imobiliaria": "DeFranco"
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
    url = "https://www.defrancoimoveis.com.br/busca/?cbOperacao=ALUGUEL&cbCidade%5B%5D=SANTA+RITA+DO+SAPUCA%C3%8D&cbBairro%5B%5D=&cbTipo=&edtCodigo=&edtCondominioMaximo=&edtValorMaximo=&edtQuartos=0&edtSuites=0&edtBanheiros=0&edtGaragens=0"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "Priority": "u=0, i",
        "Sec-Ch-Ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }

    soup = fetch_property_data(url, headers)
    if soup:
        properties = parse_property_data(soup)
        save_property_data(properties)
    else:
        print("Falha ao obter os dados dos imóveis")

if __name__ == "__main__":
    main()