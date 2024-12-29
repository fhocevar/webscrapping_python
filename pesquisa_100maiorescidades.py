import requests
import xlwt  # Biblioteca para criar arquivos Excel .xls

def consulta_empresas_100_maiores_cidades(empresa_list):
    api_key = 'AIzaSyA4AydZb5fovZ6_gaUvZcaFMMfPNNbuLKc'  # Substitua pela sua API Key válida
    dados_empresas = []

    # Lista das 100 maiores cidades do Brasil (fonte: IBGE)
    cidades_list = [
        "São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Fortaleza", "Belo Horizonte", 
        "Manaus", "Curitiba", "Recife", "Porto Alegre", "Belém", "Goiânia", "Guarulhos", 
        "Campinas", "São Luís", "São Gonçalo", "Maceió", "Duque de Caxias", "Campo Grande", 
        "Natal", "Teresina", "Osasco", "São Bernardo do Campo", "João Pessoa", "Ribeirão Preto", 
        "Nova Iguaçu", "Contagem", "Florianópolis", "Cuiabá", "Jaboatão dos Guararapes", 
        "São José dos Campos", "Santos", "Aracaju", "Feira de Santana", "Sorocaba", "Diadema", 
        "Uberlândia", "Joinville", "Aparecida de Goiânia", "Londrina", "Ananindeua", 
        "Niterói", "Belford Roxo", "Campos dos Goytacazes", "Caxias do Sul", "Macapá", 
        "Mauá", "São João de Meriti", "Santo André", "Jundiaí", "Carapicuíba", "Piracicaba", 
        "Olinda", "Campina Grande", "São José do Rio Preto", "Mogi das Cruzes", "Betim", 
        "Canoas", "Serra", "Vitória", "Bauru", "Itaquaquecetuba", "Montes Claros", 
        "Petrolina", "Boa Vista", "Vitória da Conquista", "Caucaia", "Franca", "Blumenau", 
        "Santa Maria", "Vila Velha", "Volta Redonda", "Ponta Grossa", "Marabá", 
        "Anápolis", "Pelotas", "Chapecó", "Itabuna", "Cabo de Santo Agostinho", 
        "Cascavel", "Rio Branco", "Araraquara", "Marília", "Barueri", "São Vicente", 
        "Governador Valadares", "Taubaté", "Imperatriz", "Limeira", "Suzano", "Sinop", 
        "Jequié", "Camaçari", "Itajaí", "Palmas", "Sobral", "Dourados" , "gramado" , "campos do jordão"
    ]

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

                    if len(dados_empresas) >= 100000:
                        break

            if len(dados_empresas) >= 100000:
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

    arquivo_nome = 'empresas_100_maiores_cidadesPai.xls'
    workbook.save(arquivo_nome)
    print(f"Dados salvos em {arquivo_nome} com {len(dados_empresas)} registros.")

# Exemplo de lista de empresas
#empresas = ["nutricionista", "nutrologo", "personal trainer", "pilates", "suplementos", "academia", "crossfit", "omega3", "creatina", "isotonico", "whey protein", "cha", "shake",]

# Exemplo de lista de empresas
empresas = ["suco de uva", "fertilizante", "oleo", "chocolate", "chocolatier", "confeitaria", "sorveteria", "padaria", "gelateria", "doceria", "castanhas", "nozes", "nozes macadamia", "banana passa", "nozes pecan", "castanha de caju", "atacado", "mercado", "emporio", "organicos", "castanha do para", "castanha do Brasil" , "liofilizados", "cristalizados", "frutos secos" , "cajuina", "mel", "cerveja de mel"]

# Chama a função
consulta_empresas_100_maiores_cidades(empresas)
