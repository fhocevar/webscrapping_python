import requests
import pandas as pd
from urllib.parse import quote  # Import para codificação de URLs

# Sua API Key do CNPJa
API_KEY = 'd98ef278-17e4-49b5-be0c-bcf6cc29a1f4-53c7162d-484c-4834-9e53-1df1b1c4df18'

# Lista de empresas com nome, endereço e telefone
empresas = [
    {"nome": "Armazém do Granel", "endereco": "Av. Protásio Alves, 2746 - Petrópolis, Porto Alegre - RS, 90410-006, Brazil", "telefone": "(51) 3276-8353"},
    {"nome": "Armazém dos Alimentos Orgânicos & Agroecológicos - Naturinga", "endereco": "R. Corypheu de Azevedo Marques, 292 - Vila Santo Antonio, Maringá - PR, 87030-250, Brazil", "telefone": "(44) 99944-3183"},
    {"nome": "Armazém dos Anjos Produtos Naturais", "endereco": "Av. Pedro Taques, 1456 - Zona 03, Maringá - PR, 87030-000, Brazil", "telefone": "(44) 3263-7687"},
    {"nome": "Armazém e Empório Adolpho Lisboa", "endereco": "Rua Rocha dos Santos, 59 - Centro, Manaus - AM, 69005-060, Brazil", "telefone": "(92) 3083-9043"},
    {"nome": "Armazém e Grãos - Produtos Naturais", "endereco": "Galeria Vila Nova - Av. Pedro Paes Azevedo, 784 - Sl 1 - Grageru, Aracaju - SE, 49025-570, Brazil", "telefone": "(79) 99839-0342"},
    {"nome": "Armazém Fazenda Produtos Naturais", "endereco": "Av. Anacé, 779 - Jardim Umarizal, São Paulo - SP, 05755-090, Brazil", "telefone": "(11) 2389-3938"},
    {"nome": "Armazém Fazenda Produtos Naturais", "endereco": "Estr. do Campo Limpo, 2900 - Vila Prel, São Paulo - SP, 05777-001, Brazil", "telefone": "(11) 5181-3351"},
    {"nome": "Armazém Fit Store | Imperatriz", "endereco": "R. Alagoas, 704 - Juçara, Imperatriz - MA, 65919-170, Brazil", "telefone": "(99) 98112-5086"},
    {"nome": "Armazém Fit Store Santarém | Alimentação Saudável | Suplementos | Produtos Naturais", "endereco": "Av. Mendonça Furtado, 1457 - Santa Clara, Santarém - PA, 68005-100, Brazil", "telefone": "(93) 99186-5244"},
    {"nome": "Armazém Grão Mestre - Naturais e Orgânicos", "endereco": "Rodovia Dr. Antônio Luiz Moura Gonzaga, 2975 - Rio Tavares, Florianópolis - SC, 88048-300, Brazil", "telefone": "(48) 99699-1586"},
]

# Função para consultar CNPJ usando o nome ou endereço da empresa
def consultar_cnpj(nome, endereco):
    # Codificar parâmetros para evitar problemas com caracteres especiais
    nome_codificado = quote(nome)
    endereco_codificado = quote(endereco)

    # Construir URL da requisição
    url = f"https://api.cnpja.com/companies?q={nome_codificado}&address={endereco_codificado}"
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
    cnpj = consultar_cnpj(empresa["nome"], empresa["endereco"])
    resultados.append({
        "Nome": empresa["nome"],
        "Endereço": empresa["endereco"],
        "Telefone": empresa["telefone"],
        "CNPJ": cnpj
    })

# Salvar resultados em um arquivo Excel
df = pd.DataFrame(resultados)
df.to_excel("empresas_com_cnpj.xlsx", index=False)
print("Consulta concluída. Resultados salvos em 'empresas_com_cnpj.xlsx'.")
