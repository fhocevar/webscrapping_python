import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def coletar_dados_cnpj(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Encontrar dados específicos (substitua os seletores conforme necessário)
        nome_empresa = soup.find("tag_do_nome_empresa").get_text(strip=True)
        endereco = soup.find("tag_do_endereco").get_text(strip=True)
        cnpj = soup.find("tag_do_cnpj").get_text(strip=True)

        return {
            "Nome da Empresa": nome_empresa,
            "Endereço": endereco,
            "CNPJ": cnpj
        }

    except Exception as e:
        print(f"Erro ao coletar dados: {e}")
        return None

# Lista de URLs para buscar dados (por exemplo, de uma API ou banco de dados)
urls = [
    "https://exemplo.com/empresa1",
    "https://exemplo.com/empresa2",
    # Adicione mais URLs conforme necessário
]

# Definir o User-Agent (simula um navegador)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Loop para extrair dados de várias URLs
dados = []
for url in urls:
    dados_empresa = coletar_dados_cnpj(url, headers)
    if dados_empresa:
        dados.append(dados_empresa)
    time.sleep(1)  # Pausa para evitar bloqueio

# Converter em DataFrame para exportação
df = pd.DataFrame(dados)
df.to_csv("dados_empresas.csv", index=False)
print("Dados salvos em 'dados_empresas.csv'")
