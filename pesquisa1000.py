import requests
import csv
from urllib.parse import quote

def consulta_empresas(empresa_list):
    api_key = 'AIzaSyAhquA5axfQwu49jyqym5Rd4tUin-cCZkc'  # Chave API válida
    dados_empresas = []  # Lista para armazenar os dados de todas as empresas
    
    for nome_empresa in empresa_list:
        # Codifica o nome da empresa para a URL
        nome_empresa_codificado = quote(nome_empresa)
        url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={nome_empresa_codificado}&key={api_key}'
        
        response = requests.get(url)
        data = response.json()

        # Checando se a API retornou resultados
        if 'results' in data:
            for result in data['results']:
                nome = result.get('name', 'Nome não disponível')
                endereco = result.get('formatted_address', 'Endereço não disponível')

                # Tenta pegar o telefone se disponível
                telefone = result.get('formatted_phone_number', 'Telefone não disponível')
                
                # Tenta pegar o website se disponível
                website = result.get('website', 'Website não disponível')
                
                # O nome de contato pode ser o nome da empresa, caso não tenha um campo específico
                nome_contato = result.get('name', 'Nome de contato não disponível')

                # Para o celular, consideramos um número começando com o prefixo +55 9 (Brasil)
                celular = telefone if telefone and telefone.startswith('+55 9') else 'Celular não disponível'

                # CNPJ não está disponível via Google Places API
                cnpj = 'CNPJ não disponível'

                # Armazena as informações em uma lista
                dados_empresas.append([nome, endereco, telefone, celular, website, nome_contato, cnpj])

                # Limite de 1000 registros
                if len(dados_empresas) >= 1000:
                    break

        # Se já atingiu 1000 registros, sai do loop
        if len(dados_empresas) >= 1000:
            break

    # Salvando os dados em um arquivo CSV
    with open('empresas1000.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website', 'Nome de Contato', 'CNPJ'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas.csv com {len(dados_empresas)} registros.")

# Exemplo de lista de empresas
empresas = ["castanhas", "nozes", "macadamia", "banana passa", "pecan", "caju", "atacado", "mercado", "emporio", "licor"]
consulta_empresas(empresas)
