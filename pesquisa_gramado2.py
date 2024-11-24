import requests 
import csv

def consulta_empresas(empresa_list):
    api_key = 'AIzaSyAhquA5axfQwu49jyqym5Rd4tUin-cCZkc'  # Insira sua chave de API do Google válida aqui
    dados_empresas = []  # Lista para armazenar os dados de todas as empresas
    
    def get_place_details(place_id):
        """Função para obter detalhes de um local com base no place_id."""
        url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}'
        response = requests.get(url)
        data = response.json()
        
        if 'result' in data:
            nome = data['result'].get('name', 'Nome não disponível')
            endereco = data['result'].get('formatted_address', 'Endereço não disponível')
            telefone = data['result'].get('formatted_phone_number', 'Telefone não disponível')
            cnpj = 'CNPJ não disponível'  # CNPJ não está disponível via Google Places API
            return [nome, endereco, telefone, cnpj]
        else:
            return ['Detalhes não encontrados', 'Detalhes não encontrados', 'Detalhes não encontrados', 'Detalhes não encontrados']

    for nome_empresa in empresa_list:
        # Mudança para Gramado, RS
        url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={nome_empresa}+gramado+rs&key={api_key}'
        response = requests.get(url)
        data = response.json()

        if 'results' in data:
            for result in data['results']:
                place_id = result.get('place_id')
                
                # Obtém detalhes do local usando o place_id
                if place_id:
                    dados_empresa = get_place_details(place_id)
                    dados_empresas.append(dados_empresa)

                # Limite de 1000 registros
                if len(dados_empresas) >= 1000:
                    break

        # Se já atingiu 1000 registros, sai do loop
        if len(dados_empresas) >= 1000:
            break

    # Salvando os dados em um arquivo CSV
    with open('empresas_gramado2.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'CNPJ'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_gramado2.csv com {len(dados_empresas)} registros.")

# Exemplo de lista de empresas para pesquisa
empresas = ["castanhas", "nozes", "macadamia", "banana passa", "pecan", "caju", "atacado", "mercado", "emporio", "licor", "baru", "sucos", "organicos", "para", "liofilizados", "cristalizados", "guarana"]
consulta_empresas(empresas)
