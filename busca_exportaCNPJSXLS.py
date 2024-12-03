import json
from urllib.request import Request, urlopen
from openpyxl import Workbook

# Lista de empresas
empresas = [
    "Armazém do Granel",
    "Armazém dos Alimentos Orgânicos & Agroecológicos - Naturinga",
    "Armazém dos Anjos Produtos Naturais",
    "Armazém e Empório Adolpho Lisboa",
    "Armazém e Grãos - Produtos Naturais",
    "Armazém Fazenda Produtos Naturais",
    "Armazém Fit Store | Imperatriz",
    "Armazém Fit Store Santarém | Alimentação Saudável | Suplementos | Produtos Naturais",
    "Armazém Grão Mestre - Naturais e Orgânicos"
]

# Cabeçalhos
headers = {
    'Content-Type': 'application/json',
    'authorization': 'Bearer mlvaGKAHTMiPBaBENtdhwj2pollwfFrMwaEdvxUsnsURI3CkcwqMTNMi4MOc',  # Substitua pela sua chave
    'Accept': 'application/json'
}

# URL da API
url = 'https://cnpj.biz/api/v2/empresas/listar-com-dados'

# Criação da planilha Excel
wb = Workbook()
ws = wb.active
ws.title = "Empresas CNPJ"

# Adiciona cabeçalhos na planilha
ws.append(['Razão Social', 'CNPJ', 'Status', 'Data de Abertura', 'Capital Social'])

# Loop para enviar uma requisição por vez
for empresa in empresas:
    values = json.dumps({
        "limit": 1,
        "razao_fantasia": [empresa]
    })

    request = Request(url, data=values.encode('utf-8'), headers=headers)

    try:
        response = urlopen(request)
        response_body = response.read().decode('utf-8')
        data = json.loads(response_body)

        # Extraindo os dados relevantes (ajuste conforme o retorno da API)
        if data['dados']:
            empresa_data = data['dados'][0]
            razao_social = empresa_data.get('razao_social', 'N/A')
            cnpj = empresa_data.get('cnpj', 'N/A')
            status = empresa_data.get('situacao', 'N/A')
            data_abertura = empresa_data.get('data_abertura', 'N/A')
            capital_social = empresa_data.get('capital_social', 'N/A')

            # Adiciona os dados da empresa na planilha
            ws.append([razao_social, cnpj, status, data_abertura, capital_social])

            print(f"Dados para {empresa} foram adicionados à planilha.")
        else:
            print(f"Nenhum dado encontrado para {empresa}.")
    except Exception as e:
        print(f"Erro na requisição para {empresa}: {e}")

# Salva a planilha em um arquivo Excel
wb.save("empresas_cnpjBIZ.xlsx")
print("A planilha foi salva com sucesso em 'empresas_cnpjBIZ.xlsx'")
