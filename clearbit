import requests
import csv

def consulta_empresas_clearbit(empresa_list):
    api_key = 'SUA_CLEARBIT_API_KEY'  # Substitua pela sua chave API válida
    dados_empresas = []  # Lista para armazenar os dados de todas as empresas
    
    for nome_empresa in empresa_list:
        # O Clearbit aceita domínios, então você pode tentar buscar o domínio da empresa
        url = f'https://company.clearbit.com/v2/companies/find?name={nome_empresa}'
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.get(url, headers=headers)
        data = response.json()

        if 'name' in data:
            nome = data.get('name', 'Nome não disponível')
            endereco = data.get('location', 'Endereço não disponível')
            telefone = data.get('phone', 'Telefone não disponível')
            email = data.get('email', 'Email não disponível')
            cnpj = 'CNPJ não disponível'  # Clearbit não fornece CNPJ diretamente

            # Armazena as informações em uma lista
            dados_empresas.append([nome, endereco, telefone, email, cnpj])

            # Limite de 100 registros
            if len(dados_empresas) >= 100:
                break

        # Se já atingiu 100 registros, sai do loop
        if len(dados_empresas) >= 100:
            break

    # Salvando os dados em um arquivo CSV
    with open('empresas_clearbit.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Email', 'CNPJ'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_clearbit.csv com {len(dados_empresas)} registros.")

# Exemplo de lista de empresas
empresas = ["Loja de Castanhas", "Mercado Castanhas", "Escritório Castanhas"]
consulta_empresas_clearbit(empresas)
