import requests
import csv

def consulta_mercados_municipais():
    api_key = 'AIzaSyAhquA5axfQwu49jyqym5Rd4tUin-cCZkc'  # Substitua pela sua chave válida da API do Google
    capitais = {
        "AC": "Rio Branco",
        "AL": "Maceió",
        "AP": "Macapá",
        "AM": "Manaus",
        "BA": "Salvador",
        "CE": "Fortaleza",
        "DF": "Brasília",
        "ES": "Vitória",
        "GO": "Goiânia",
        "MA": "São Luís",
        "MT": "Cuiabá",
        "MS": "Campo Grande",
        "MG": "Belo Horizonte",
        "PA": "Belém",
        "PB": "João Pessoa",
        "PR": "Curitiba",
        "PE": "Recife",
        "PI": "Teresina",
        "RJ": "Rio de Janeiro",
        "RN": "Natal",
        "RS": "Porto Alegre",
        "RO": "Porto Velho",
        "RR": "Boa Vista",
        "SC": "Florianópolis",
        "SP": "São Paulo",
        "SP": "GUARULHOS",
        "SP": "CAMPINAS",
        "SE": "Aracaju",
        "TO": "Palmas",
    }

    dados_mercados = []

    for estado, capital in capitais.items():
        query = f"Mercado Municipal {capital}"
        url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={api_key}'
        
        response = requests.get(url)
        data = response.json()

        if 'results' in data:
            for result in data['results']:
                nome = result.get('name', 'Nome não disponível')
                endereco = result.get('formatted_address', 'Endereço não disponível')
                telefone = 'Telefone não disponível'  # Não disponível com Text Search
                cnpj = 'CNPJ não disponível'  # Não disponível via Google Places API

                dados_mercados.append([estado, capital, nome, endereco, telefone, cnpj])

    # Salvando os dados em um arquivo CSV
    with open('mercados_municipais.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Estado', 'Capital', 'Nome', 'Endereço', 'Telefone', 'CNPJ'])  # Cabeçalho
        writer.writerows(dados_mercados)

    print(f"Dados salvos em mercados_municipais.csv com {len(dados_mercados)} registros.")

# Executar a consulta
consulta_mercados_municipais()
