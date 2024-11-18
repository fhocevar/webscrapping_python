import requests
import csv

def consulta_empresas_hunter(empresa_list):
    api_key = 'ac032af147f0b4620abb967206f028aea84b379a'  # Substitua pela sua chave API válida
    dados_empresas = []  # Lista para armazenar os dados de todas as empresas
    
    for nome_empresa in empresa_list:
        # Você precisa de um domínio para realizar a pesquisa (simulando uma busca com um domínio fictício)
        domain = f"{nome_empresa.replace(' ', '').lower()}.com"  # Exemplo de domínio fictício
        url = f'https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}'
        response = requests.get(url)
        data = response.json()

        if 'data' in data and 'emails' in data['data']:
            emails = data['data']['emails']
            email = emails[0]['value'] if emails else 'Email não disponível'
            nome = nome_empresa
            endereco = 'Endereço não disponível'
            telefone = 'Telefone não disponível'
            cnpj = 'CNPJ não disponível'  # Hunter.io não fornece CNPJ diretamente

            # Armazena as informações em uma lista
            dados_empresas.append([nome, endereco, telefone, email, cnpj])

            # Limite de 100 registros
            if len(dados_empresas) >= 100:
                break

        # Se já atingiu 100 registros, sai do loop
        if len(dados_empresas) >= 100:
            break

    # Salvando os dados em um arquivo CSV
    with open('empresas_hunter.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Email', 'CNPJ'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_hunter.csv com {len(dados_empresas)} registros.")

# Exemplo de lista de empresas
empresas = ["Loja de Castanhas", "Mercado Castanhas", "Escritório Castanhas"]
consulta_empresas_hunter(empresas)
