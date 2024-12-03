import json
from urllib.request import Request, urlopen

# Corpo da requisição
values = """
{
  "limit": 1,
  "razao_fantasia": [
    "Armazém do Granel"
  ]
}
"""

# Cabeçalhos
headers = {
    'Content-Type': 'application/json',
    'authorization': 'Bearer mlvaGKAHTMiPBaBENtdhwj2pollwfFrMwaEdvxUsnsURI3CkcwqMTNMi4MOc',  # Substitua pela sua chave
    'Accept': 'application/json'
}

# URL
url = 'https://cnpj.biz/api/v2/empresas/listar-com-dados'
request = Request(url, data=values.encode('utf-8'), headers=headers)

# Fazer requisição
try:
    response = urlopen(request)
    response_body = response.read().decode('utf-8')
    data = json.loads(response_body)

    # Exibe os dados
    print(json.dumps(data, indent=2, ensure_ascii=False))
except Exception as e:
    import traceback
    print(f"Erro na requisição: {e}")
    traceback.print_exc()
