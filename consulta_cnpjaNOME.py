import requests
import pandas as pd
from urllib.parse import quote  # Import para codificação de URLs

# Sua API Key do CNPJa
API_KEY = 'd98ef278-17e4-49b5-be0c-bcf6cc29a1f4-53c7162d-484c-4834-9e53-1df1b1c4df18'

# Lista de empresas com nome
empresas = [
    {"nome": "Armazém do Granel"},
    {"nome": "Armazém dos Alimentos Orgânicos & Agroecológicos - Naturinga"},
    {"nome": "Armazém dos Anjos Produtos Naturais"},
    {"nome": "Armazém e Empório Adolpho Lisboa"},
    {"nome": "Armazém e Grãos - Produtos Naturais"},
    {"nome": "Armazém Fazenda Produtos Naturais"},
    {"nome": "Armazém Fazenda Produtos Naturais"},
    {"nome": "Armazém Fit Store | Imperatriz"},
    {"nome": "Armazém Fit Store Santarém | Alimentação Saudável | Suplementos | Produtos Naturais"},
    {"nome": "Armazém Grão Mestre - Naturais e Orgânicos"}
]

# Função para consultar CNPJ usando o nome da empresa
def consultar_cnpj(nome):
    # Codificar parâmetro para evitar problemas com caracteres especiais
    nome_codificado = quote(nome)

    # Construir URL da requisição
    url = f"https://api.cnpja.com/companies?q={nome_codificado}"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    try:
        # Realizar a requisição GET
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Garante que códigos HTTP de erro sejam tratados

        # Processar resposta
        data = response.json()
        if data and "data" in data and data["data"]:
            return data["data"][0].get("cnpj", "CNPJ não encontrado")
        else:
            return "CNPJ não encontrado"
    except requests.exceptions.RequestException as e:
        # Lidar com possíveis erros de rede ou API
        print(f"Erro na consulta: {e}")
        return "Erro na consulta"

# Consultar todas as empresas e armazenar resultados
resultados = []
for i, empresa in enumerate(empresas, start=1):
    print(f"Consultando {i}/{len(empresas)}: {empresa['nome']}")
    cnpj = consultar_cnpj(empresa["nome"])
    resultados.append({
        "Nome": empresa["nome"],
        "CNPJ": cnpj
    })

# Salvar resultados em um arquivo Excel
df = pd.DataFrame(resultados)
df.to_excel("empresas_com_cnpj.xlsx", index=False)
print("Consulta concluída. Resultados salvos em 'empresas_com_cnpj.xlsx'.")
