import requests 
import csv

def consulta_empresas(empresa_list):
    api_key = 'AIzaSyAhquA5axfQwu49jyqym5Rd4tUin-cCZkc'  # Mantendo sua chave de API do Google aqui
    dados_empresas = []  # Lista para armazenar os dados de todas as empresas
    
    for nome_empresa in empresa_list:
        # Mudança para Campo Grande, MS
        url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={nome_empresa}+Campo+Grande+MS&key={api_key}'
        response = requests.get(url)
        data = response.json()

        if 'results' in data:
            for result in data['results']:
                nome = result.get('name', 'Nome não disponível')
                endereco = result.get('formatted_address', 'Endereço não disponível')
                telefone = 'Telefone não disponível'  # A Text Search API não retorna telefone diretamente
                cnpj = 'CNPJ não disponível'  # CNPJ não está disponível via Google Places API

                # Armazena as informações em uma lista
                dados_empresas.append([nome, endereco, telefone, cnpj])

                # Limite de 1000 registros
                if len(dados_empresas) >= 1000:
                    break

        # Se já atingiu 1000 registros, sai do loop
        if len(dados_empresas) >= 1000:
            break

    # Salvando os dados em um arquivo CSV
    with open('empresas_CampoGrande.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'CNPJ'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_CampoGrande.csv com {len(dados_empresas)} registros.")

# Exemplo de lista de empresas para pesquisa
empresas = ["castanhas", "nozes", "macadamia", "banana passa", "pecan", "caju", "atacado", "mercado", "emporio", "licor", "baru", "sucos", "organicos", "liofilizados", "cristalizados", "guarana"]
consulta_empresas(empresas)
