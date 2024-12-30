import requests

api_key = 'AIzaSyBUJin_uNG9_1_ZMfJFuhfnje8b3zYk_ow'  # Coloque sua chave aqui

# Teste simples da API para verificar se a chave está funcionando
url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurants&key={api_key}'
response = requests.get(url)
data = response.json()

if 'error_message' in data:
    print(f"Erro: {data['error_message']}")
else:
    print("A chave de API está funcionando corretamente. Dados recebidos:", data)
