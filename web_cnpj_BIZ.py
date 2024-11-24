import requests
import csv

def buscar_cnpjs(empresa_list, api_key):
    url_base = "https://api.cnpj.biz/v1/companies"
    headers = {"Authorization": f"Bearer {api_key}"}
    dados_empresas = []

    for nome_empresa in empresa_list:
        params = {"name": nome_empresa}  # Parâmetro para buscar por nome
        try:
            response = requests.get(url_base, headers=headers, params=params)
            if response.status_code == 200:
                resultados = response.json()
                # Itera pelos resultados encontrados
                for resultado in resultados:
                    cnpj = resultado.get("cnpj", "CNPJ não encontrado")
                    nome = resultado.get("name", "Nome não encontrado")
                    endereco = resultado.get("address", "Endereço não encontrado")
                    telefone = resultado.get("phone", "Telefone não encontrado")
                    
                    dados_empresas.append([nome, cnpj, endereco, telefone])
            else:
                print(f"Erro ao buscar {nome_empresa}: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Erro ao consultar a empresa {nome_empresa}: {e}")

    # Salvando em arquivo CSV
    with open('empresas_cnpjs.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'CNPJ', 'Endereço', 'Telefone'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Consulta finalizada! Dados salvos em 'empresas_cnpjs.csv'.")

# Exemplo de lista de empresas
empresas = ["Jacastanhas", "Empório das Castanhas", "Noz do Brasil", "Supermercado Castanha"]
api_key = "mlvaGKAHTMiPBaBENtdhwj2pollwfFrMwaEdvxUsnsURI3CkcwqMTNMi4MOc"

# Executa a consulta
buscar_cnpjs(empresas, api_key)
