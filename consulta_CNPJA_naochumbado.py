import requests
import pandas as pd

# Configurações da API
API_KEY = "009f8590-4f11-463e-85d4-60a46f47600c-d895a848-e22c-4cb8-a325-e3d809bd232a"
BASE_URL = "https://api.cnpja.com.br/companies"

# Carregar a lista de empresas
input_file = "empresas.xlsx"  # Nome do arquivo de entrada
empresas = pd.read_excel(input_file)

# Função para consultar a API
def buscar_cnpj(nome, endereco):
    try:
        params = {"name": nome, "address": endereco}
        headers = {"Authorization": f"Bearer {API_KEY}"}
        response = requests.get(BASE_URL, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            # Retorna o primeiro CNPJ encontrado
            return data.get("companies", [{}])[0].get("cnpj", "CNPJ não encontrado")
        else:
            print(f"Erro na consulta: {response.status_code}")
            return "Erro na consulta"
    except Exception as e:
        print(f"Erro: {e}")
        return "Erro ao consultar"

# Adicionar CNPJ à tabela de empresas
empresas["CNPJ"] = empresas.apply(lambda x: buscar_cnpj(x["Nome"], x["Endereço"]), axis=1)

# Salvar os resultados em um novo arquivo
empresas.to_excel("empresas_com_cnpj.xlsx", index=False)
print("Arquivo gerado com sucesso!")
