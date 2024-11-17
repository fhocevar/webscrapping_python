import requests

def consulta_empresas(empresa_list):
    api_key = 'AIzaSyAhquA5axfQwu49jyqym5Rd4tUin-cCZkc'
    
    for nome_empresa in empresa_list:
        url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={nome_empresa}&key={api_key}'
        response = requests.get(url)
        data = response.json()

        if 'results' in data:
            for result in data['results']:
                nome = result.get('name')
                telefone = result.get('formatted_phone_number', 'Telefone não disponível')
                print(f"Nome: {nome}, Telefone: {telefone}")
        else:
            print(f"Não encontrado: {nome_empresa}")

# Exemplo de lista de empresas
empresas = ["Restaurante Exemplo", "Loja ABC", "Escritório XYZ"]
consulta_empresas(empresas)
