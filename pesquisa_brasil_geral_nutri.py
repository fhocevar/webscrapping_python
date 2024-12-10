import requests
import xlwt  # Biblioteca para criar arquivos Excel .xls

def obter_cidades_brasil():
    """Função para obter uma lista completa de cidades do Brasil."""
    # URL com todos os municípios brasileiros disponíveis na API do IBGE
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
    response = requests.get(url)
    if response.status_code == 200:
        municipios = response.json()
        # Extrai os nomes das cidades
        return [municipio["nome"] for municipio in municipios]
    else:
        print("Erro ao obter lista de municípios.")
        return []

def consulta_empresas(empresa_list):
    api_key = 'AIzaSyA4AydZb5fovZ6_gaUvZcaFMMfPNNbuLKc'  # Substitua pela sua API Key válida
    dados_empresas = []

    def get_place_details(place_id):
        url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}'
        response = requests.get(url)
        data = response.json()
        
        if 'result' in data:
            nome = data['result'].get('name', 'Nome não disponível').replace('\n', ' ').replace('\r', '')
            endereco = data['result'].get('formatted_address', 'Endereço não disponível').replace('\n', ' ').replace('\r', '')
            telefone = data['result'].get('formatted_phone_number', 'Telefone não disponível').replace('\n', ' ').replace('\r', '')           
            return [nome, endereco, telefone]
        else:
            return ['Detalhes não encontrados', 'Detalhes não encontrados', 'Detalhes não encontrados']

    cidades_list = obter_cidades_brasil()  # Obter lista de cidades do Brasil
    for nome_empresa in empresa_list:
        for cidade in cidades_list:
            url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={nome_empresa}+{cidade}&region=br&key={api_key}'
            response = requests.get(url)
            data = response.json()

            if 'results' in data:
                for result in data['results']:
                    place_id = result.get('place_id')
                    
                    if place_id:
                        dados_empresa = get_place_details(place_id)
                        dados_empresas.append(dados_empresa)

                    if len(dados_empresas) >= 1000000:
                        break

            if len(dados_empresas) >= 1000000:
                break

    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('Empresas')

    sheet.write(0, 0, 'Nome')
    sheet.write(0, 1, 'Endereço')
    sheet.write(0, 2, 'Telefone')

    sheet.col(0).width = 256 * 30
    sheet.col(1).width = 256 * 50
    sheet.col(2).width = 256 * 20

    for i, linha in enumerate(dados_empresas, start=1):
        sheet.write(i, 0, linha[0])
        sheet.write(i, 1, linha[1])
        sheet.write(i, 2, linha[2])

    arquivo_nome = 'empresas_todo_brasil.xls'
    workbook.save(arquivo_nome)
    print(f"Dados salvos em {arquivo_nome} com {len(dados_empresas)} registros.")

# Exemplo de lista de empresas
empresas = ["nutricionista", "nutrologo", "personal trainer", "pilates", "suplementos", "academia", "crossfit", "omega3", "creatina", "isotonico", "whey protein", "cha", "shake",]

# Chama a função
consulta_empresas(empresas)
