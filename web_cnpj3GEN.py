import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Carrega os dados (supondo que estão em um arquivo CSV com colunas "Nome", "Endereço" e "Telefone")
dados_empresas = pd.read_csv("lista_empresas.csv")

# Função para buscar o CNPJ usando os dados da empresa
def buscar_cnpj(nome, endereco, telefone, headers):
    try:
        # Substitua "url_base" pela URL do site que permite consultas usando esses dados
        # e ajuste os parâmetros conforme necessário
        url = f"https://exemplo.com/buscar?nome={nome}&endereco={endereco}&telefone={telefone}"
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extrai o CNPJ da página (ajuste o seletor conforme a estrutura HTML)
        cnpj = soup.find("tag_do_cnpj").get_text(strip=True)
        
        return cnpj

    except Exception as e:
        print(f"Erro ao buscar CNPJ para {nome}: {e}")
        return None

# Definir o User-Agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Adiciona uma coluna de CNPJ no DataFrame para salvar os resultados
dados_empresas['CNPJ'] = None

# Loop para buscar CNPJ de cada empresa
for index, row in dados_empresas.iterrows():
    nome = row['Nome']
    endereco = row['Endereço']
    telefone = row['Telefone']
    
    # Busca o CNPJ e salva no DataFrame
    cnpj = buscar_cnpj(nome, endereco, telefone, headers)
    dados_empresas.at[index, 'CNPJ'] = cnpj
    time.sleep(1)  # Pausa para evitar bloqueio

# Salva o resultado em um novo CSV
dados_empresas.to_csv("dados_empresas_com_cnpj.csv", index=False)
print("Dados com CNPJ salvos em 'dados_empresas_com_cnpj.csv'")
