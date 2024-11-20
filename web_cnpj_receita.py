import requests
import csv

def consulta_empresas_cnpj(empresa_list):
    api_key = '69712d9ad8116ce5e8b8ba86aa82d2ebc69123cf76c9bab24c5c783d66feb7ae'  # Substitua pela sua chave do ReceitaWS
    url_base = 'https://www.receitaws.com.br/v1/cnpj/'
    dados_empresas = []

    for nome_empresa in empresa_list:
        try:
            # Adaptação para simular consulta por nome na API ReceitaWS
            print(f"Consultando {nome_empresa}...")
            url = f'https://www.receitaws.com.br/v1/cnpj/{nome_empresa}?token={api_key}'  # Ajuste conforme documentação

            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()

                cnpj = data.get('cnpj', 'CNPJ não encontrado')
                nome = data.get('nome', nome_empresa)
                endereco = data.get('logradouro', '') + ', ' + data.get('numero', '')
                telefone = data.get('telefone', 'Telefone não encontrado')

                dados_empresas.append([nome, cnpj, endereco, telefone])
            else:
                dados_empresas.append([nome_empresa, 'CNPJ não encontrado', 'Endereço não encontrado', 'Telefone não encontrado'])

        except Exception as e:
            print(f"Erro ao consultar {nome_empresa}: {e}")
            dados_empresas.append([nome_empresa, 'Erro na consulta', 'Erro na consulta', 'Erro na consulta'])

    # Salvando os dados em um arquivo CSV
    with open('empresas_com_cnpj.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'CNPJ', 'Endereço', 'Telefone'])
        writer.writerows(dados_empresas)

    print(f"Dados salvos em empresas_com_cnpj.csv com {len(dados_empresas)} registros.")

# Lista de empresas
empresas = ["Noz do Brasil - Produtos Naturais - Vila Prudente SP", "Empório das Castanhas", "Supermercado Castanha", "Empório Santa Castanha",
    "EMPÓRIO ROSA - ZONA CEREALISTA", "Pedro das Castanhas", "Empório La Granola - Produtos Naturais a Granel", "Nutty Bavarian", 
    "Mercadão Natural", "Empório Granum", "Paulistinha Alimentos - Culinária Natural, Nordestina e Africana", "Armazém Sabores a Granel",
    "M.J. Doces E Castanhas", "Bendito Grão", "EMPÓRIO DG NATURAIS CASTANHAS", "Castanhão Atacadista", "Tetê Castanha | Flores", 
    "Residencial Pecan", "Brazilian Nuts - Açaí, sucos e castanhas - Vila Madalena, São Paulo", "Empório Caju - Cerealista",
    "Fazenda Paulista Grãos e Cereais", "Mooca Buns - Brooklin", "Malu Mar Pescados", "Bakebun Bakery Bela Vista", "Cinnamon Land", 
    "Vila Caju", "Caju Bar", "Boteco do Juca", "Lanchonete e Restaurante Caju Verde", "Restaurante Caju Verde", 
    "Lanchonete Nova Skina Caju Verde", "Restaurante Cajueiro Água Fria", "Comunidade CaJu", "Caju Chihuahua", "Atacadista São Paulo Com. Imp. Ltda", 
    "Wholesale São Paulo", "Atacado São Paulo", "Yacima - Wholesale Lingerie - Bras - São Paulo - SP", "Sampa Atacado - Av do Estado", 
    "25 de março atacado e varejo", "BAIP Produtos Populares Distribuidora Atacadista", "Roupas Atacado SP, Atacado de Roupas em São Paulo - Griffe Atacado", 
    "NIKATO ATACADISTA", "R25 Atacadista", "Atento Atacadista Brás", "Distributor Wilson de Calçados", "Super Balance Wholesale", 
    "Issam Distribuidora - Nacionais e Importados", "Super Wholesale Magno", "Yanai", "3 Dantas Comercial Atacadista", "L4 Comercial Ltda", 
    "Atacado Barato Varejo", "Mercado Municipal Paulistano", "Mercado Municipal de Pinheiros", "Municipal Market Pari", "Mercado público são paulo", 
    "Pão de Açúcar", "Carnes Mercado Central - A Melhor Distribuidora De São Paulo", "Municipal market Kinjo Yamato", "Emporium São Paulo", 
    "Santa Maria Empório Cidade Jardim", "Empório São Bento", "Empório Fernandes Pinheiros", "Empório Datavenia", "EMPORIO CEREALISTA POMPEIA", 
    "Casa Garcia - Desde 1968", "Marula Artesanal Morin - Licor", "Licoretto Bebidas", "Imigrantes Bebidas", "Empório Frades", "Adega Do Alê", 
    "Beale Bebidas", "Empório Frei Caneca", "Rei dos Whisky's & Vinhos Liquor Store", "Adega La Casa das Bebidas", "Liquore di Famiglia - Licores artesanais", 
    "Empório Luso, Água Mineral, Vinhos e licores", "Cachaçaria SP Empório", "Quetzalli Drink", "All Shopping das Bebidas", "Cia. Whiskey", 
    "Bebidas em Casa", "Licor Novidades"
]
consulta_empresas_cnpj(empresas)
