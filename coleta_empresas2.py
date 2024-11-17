import requests

def consulta_empresas(empresa_list):
    api_key = 'AIzaSyAhquA5axfQwu49jyqym5Rd4tUin-cCZkc'  # Substitua pela sua chave API válida
    
    for nome_empresa in empresa_list:
        url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={nome_empresa}&key={api_key}'
        response = requests.get(url)
        data = response.json()

        if 'results' in data:
            for result in data['results']:
                nome = result.get('name', 'Nome não disponível')
                endereco = result.get('formatted_address', 'Endereço não disponível')
                telefone = result.get('formatted_phone_number', 'Telefone não disponível')
                
                # Para pegar o CNPJ, seria necessário outra fonte, como uma API específica de dados de empresas ou scraping.
                cnpj = 'CNPJ não disponível'  # Para CNPJ, o ideal seria buscar em outro lugar como Receita Federal.

                # Imprime os dados coletados
                print(f"Nome: {nome}")
                print(f"Endereço: {endereco}")
                print(f"Telefone: {telefone}")
                print(f"CNPJ: {cnpj}")
                print('-' * 40)
        else:
            print(f"Não encontrado: {nome_empresa}")

# Exemplo de lista de empresas
empresas = ["loja de castanhas", "mercado castanhas", "Escritório castanhas"]
consulta_empresas(empresas)
