import requests
import xlwt  # Biblioteca para criar arquivos Excel .xls

def consulta_empresas(empresa_list, cidades_list):
    api_key = 'AIzaSyBUJin_uNG9_1_ZMfJFuhfnje8b3zYk_ow'  # Insira sua chave de API do Google válida aqui
    dados_empresas = []  # Lista para armazenar os dados de todas as empresas
    
    def get_place_details(place_id):
        """Função para obter detalhes de um local com base no place_id."""
        url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}'
        response = requests.get(url)
        data = response.json()
        
        if 'result' in data:
            nome = data['result'].get('name', 'Nome não disponível').replace('\n', ' ').replace('\r', ' ')
            endereco = data['result'].get('formatted_address', 'Endereço não disponível').replace('\n', ' ').replace('\r', ' ')
            telefone = data['result'].get('formatted_phone_number', 'Telefone não disponível').replace('\n', ' ').replace('\r', '')
            website = data['result'].get('website', 'Site não disponível')  # Tentando pegar o site
            # Tentativa de pegar e-mail (não garantido pela API)
            email = 'E-mail não disponível'  # Como não há campo específico de e-mail, podemos tentar pegar do site (se presente)
            return [nome, endereco, telefone, website, email]
        else:
            return ['Detalhes não encontrados', 'Detalhes não encontrados', 'Detalhes não encontrados', 'Detalhes não encontrados', 'Detalhes não encontrados']

    for nome_empresa in empresa_list:
        for cidade in cidades_list:
            url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={nome_empresa}+{cidade}&key={api_key}'
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
                    if len(dados_empresas) >= 100000:
                        break

            # Se já atingiu 1000 registros, sai do loop
            if len(dados_empresas) >= 100000:
                break

    # Salvando os dados em um arquivo Excel .xls
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('Empresas')

    # Cabeçalhos (escritos na primeira linha)
    sheet.write(0, 0, 'Nome')
    sheet.write(0, 1, 'Endereço')
    sheet.write(0, 2, 'Telefone')
    sheet.write(0, 3, 'Website')
    sheet.write(0, 4, 'E-mail')

    # Ajuste de largura das colunas
    sheet.col(0).width = 256 * 30  # Coluna Nome - 30 caracteres
    sheet.col(1).width = 256 * 50  # Coluna Endereço - 50 caracteres
    sheet.col(2).width = 256 * 20  # Coluna Telefone - 20 caracteres
    sheet.col(3).width = 256 * 50  # Coluna Website - 50 caracteres
    sheet.col(4).width = 256 * 30  # Coluna E-mail - 30 caracteres

    # Adiciona os dados em LINHAS consecutivas
    for i, linha in enumerate(dados_empresas, start=1):  # Começa na linha 1 (linha 0 é o cabeçalho)
        sheet.write(i, 0, linha[0])  # Nome na coluna 0
        sheet.write(i, 1, linha[1])  # Endereço na coluna 1
        sheet.write(i, 2, linha[2])  # Telefone na coluna 2
        sheet.write(i, 3, linha[3])  # Website na coluna 3
        sheet.write(i, 4, linha[4])  # E-mail na coluna 4

    # Salva o arquivo
    arquivo_nome = 'empresas_multicidades_brasil.xls'
    workbook.save(arquivo_nome)
    print(f"Dados salvos em {arquivo_nome} com {len(dados_empresas)} registros.")

# Exemplo de lista de empresas para pesquisa
empresas = ["castanhas", "nozes", "nozes macadamia", "banana passa", "nozes pecan", "castanha de caju", "atacado", "mercado", "emporio", "organicos", "castanha do para", "castanha do Brasil" , "liofilizados", "cristalizados", "frutos secos" , "cajuina", "gelatos", "sorveteria", "padaria", "confeitaria", "fertilizante", "vinagre","chocolate", "chocolatier", "confeitaria", "sorveteria", "padaria", "gelateria", "doceria","castanhas", "nozes", "nozes macadamia", "banana passa", "nozes pecan", "castanha de caju", "atacado", "mercado", "emporio", "organicos", "castanha do para", "castanha do Brasil" , "liofilizados", "cristalizados", "frutos secos" , "cajuina", "gelatos", "sorveteria", "padaria", "confeitaria", "fertilizante", "vinagre","suco de uva", "suco de mexirica", "vinagre de mel", "vinagre", "fertilizante", "oleo", "oleo de pecan", "oleo de macadamia" ]

# Lista de cidades
cidades = ["brasilia", "sao paulo", "porto alegre", "blumenau","curitiba", "joinville", "florianopolis", "santarem", "riodejaneiro", "saogoncalo", "belem", "salvador", "aracaju", "maceio", "manaus", "campogrande", "portovelho", "riobranco", "campinas", "guarulhos", "cuiaba", "belo horizonte", "uberlandia", "uberaba", "teresina", "recife", "macapa" , "imperatriz" , "gramado" , "maringa" , "fozdoiguacu", "boavista",]

# Chama a função
consulta_empresas(empresas, cidades)
