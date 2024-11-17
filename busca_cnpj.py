import requests

def consulta_cnpj(cnpj):
    url = f"https://www.cnpj.ws/api/empresa/{cnpj}"
    headers = {'Authorization': 'Bearer SUA_CHAVE_API'}
    response = requests.get(url, headers=headers)
    data = response.json()
    
    if data.get('status') == 'OK':
        return data['data']  # Retorna os dados do CNPJ
    else:
        return "CNPJ não encontrado."

# Exemplo de busca
cnpj_info = consulta_cnpj("12345678000195")  # Substitua por um CNPJ válido
print(cnpj_info)
