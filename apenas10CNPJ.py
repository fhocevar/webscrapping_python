import json
from urllib.request import Request, urlopen

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

# URL
url = 'https://cnpj.biz/api/v2/empresas/listar-com-dados'

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

        # Exibe os dados
        print(f"Dados para {empresa}:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Erro na requisição para {empresa}: {e}")
