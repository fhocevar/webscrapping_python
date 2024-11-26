import requests
import csv

def consulta_cnpj_serasa(nomes_empresas, api_key):
    """Consulta os CNPJs de uma lista de empresas por meio da API do Serasa."""

    dados_empresas = []  # Lista para armazenar os dados de todas as empresas
    
    for nome_empresa in nomes_empresas:
        # Monta a URL da API do Serasa (URL fictícia como exemplo)
        url = f'https://api.serasaexperian.com.br/consulta_cnpj?nome_empresa={nome_empresa}&api_key={api_key}'
        
        # Realiza a requisição
        response = requests.get(url)
        
        # Verifica se a resposta é bem-sucedida
        if response.status_code == 200:
            data = response.json()
            # Extrai os dados necessários
            nome = data.get('nome', 'Nome não disponível')
            cnpj = data.get('cnpj', 'CNPJ não disponível')
            endereco = data.get('endereco', 'Endereço não disponível')
            telefone = data.get('telefone', 'Telefone não disponível')
            
            # Adiciona aos dados de empresas
            dados_empresas.append([nome, cnpj, endereco, telefone])
        else:
            print(f"Não foi possível consultar dados para {nome_empresa}. Status {response.status_code}")

    # Salva os dados em um arquivo CSV
    with open('empresas_serasa.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'CNPJ', 'Endereço', 'Telefone'])  # Cabeçalho
        writer.writerows(dados_empresas)

    print(f"Dados salvos em empresas_serasa.csv com {len(dados_empresas)} registros.")

# Lista de nomes de empresas para consulta
nomes_empresas = ["Nome Empresa 1", "Nome Empresa 2", "Nome Empresa 3"]
api_key = "SUA_API_KEY_SERASA"

consulta_cnpj_serasa(nomes_empresas, api_key)
