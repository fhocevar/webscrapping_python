from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
from urllib.parse import quote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Função para configurar o Selenium com o WebDriverManager
def configurar_navegador():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Para rodar em modo sem interface gráfica
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Configura o ChromeDriver com WebDriverManager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Função para realizar a consulta e coletar os dados das empresas
def consulta_empresas(empresa_list):
    driver = configurar_navegador()  # Inicializa o navegador
    dados_empresas = []

    for nome_empresa in empresa_list:
        nome_empresa_codificado = quote(nome_empresa)  # Codifica o nome da empresa para a URL
        url = f'https://www.google.com/search?q={nome_empresa_codificado}'
        driver.get(url)
        time.sleep(5)  # Aguarda o carregamento da página

        # Coleta informações dos resultados da busca
        try:
            # Espera explícita para garantir que o nome da empresa seja carregado
            nome_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h3'))
            )
            nome = nome_element.text.strip()

            # Coleta o endereço
            endereco = driver.find_element(By.XPATH, '//span[contains(text(),"endereço")]/parent::div').text.strip() if driver.find_elements(By.XPATH, '//span[contains(text(),"endereço")]') else 'Endereço não disponível'
            
            # Buscando o telefone ou celular de forma mais flexível
            telefone = ''
            celular = ''
            if driver.find_elements(By.XPATH, '//span[contains(text(),"Telefone")]/parent::div'):
                telefone = driver.find_element(By.XPATH, '//span[contains(text(),"Telefone")]/parent::div').text.strip()
            if driver.find_elements(By.XPATH, '//span[contains(text(),"celular")]/parent::div'):
                celular = driver.find_element(By.XPATH, '//span[contains(text(),"celular")]/parent::div').text.strip()
            
            # Detectando telefone com base no formato +55 ou (DDD) 9
            if telefone and (telefone.startswith('+55') or telefone.startswith('9')):
                celular = telefone  # Considera o número como celular se tiver DDD 9 ou formato internacional

            # Espera explícita para o website
            website_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "http")]'))
            )
            website = website_element.get_attribute('href') if website_element else 'Website não disponível'

            dados_empresas.append([nome, endereco, telefone, celular, website])

        except Exception as e:
            print(f"Erro ao buscar {nome_empresa}: {e}")
            dados_empresas.append([nome_empresa, 'Não encontrado', 'Não encontrado', 'Não encontrado', 'Não encontrado'])

    driver.quit()  # Fecha o navegador

    # Salvando os dados em um arquivo CSV
    with open('empresas130_testando4.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas.csv com {len(dados_empresas)} registros.")

# Lista de empresas fornecida por você
empresas = [
    "Casa Santa Luzia", "Distribuidora Green Market", "Empório Nutri Nuts", "Natus Nuts", "Ki-Caju", "Nutty Bavarian",
    "Amêndoa Distribuidora", "Nutty Nuts", "Grão de Gente", "Atacado Vila Nova", "Central Nogueira", "MixNut Distribuidora",
    "Zamin Nuts", "Vila Granel", "Nutra Nuts", "Castanha do Brasil", "Grão & Cia Distribuidora", "Mercadão Municipal (Zona Cerealista)",
    "Distribuidora NutriCoop", "Casa Flora", "Giroil", "SuperFoods Brasil", "LeManjue Organics Distribuidora", "Bella Mix Produtos Naturais",
    "Castanha Mix Distribuidora", "Nutri Import", "Gran Nuts", "Litoral Produtos Naturais", "Atacado da Castanha", "Distribuidora Hortelã",
    "Comercial Vitória", "Nutsland", "Brasil Nuts", "Central de Grãos e Castanhas", "Empório Terra Madre", "Atacado Frutos da Terra",
    "Mundo dos Grãos", "Distribuidora Viva Alimentos Naturais", "Simples & Natural - Grãos e Castanhas", "Noz do Brasil - Produtos Naturais - Vila Prudente SP",
    "Nutty Up", "Empório das Castanhas", "M.J. Doces E Castanhas", "Supermercado Castanha", "Mercadão Natural", "Empório Zanata",
    "Empório Santa Castanha", "Brazilian Nuts - Açaí, sucos e castanhas - Vila Madalena, São Paulo", "Armazém Paes e Paes Zona Cerealista do ABC",
    "EMPÓRIO SETE MESTRES", "Macadâmia Cerealista LTDA", "MACADÂMIA MERCADO SAUDÁVEL", "Macadamia Bolsas e Acessórios", "Macadâmia Home",
    "Macadâmia moda feminina", "Mr. Cheney - Cookies", "Biscoitê A Biscoiteira", "Dadiva Natural - Loja de Produtos Naturais Santo André",
    "Macadâmia Bela Vista", "Restaurante Bananeira", "Pecan Restaurante - Shop. Paineiras", "Residencial Pecan", "Pecan Móveis Planejados",
    "Loteamento Fechado Pecan (Lotes a partir de 360 M2)", "Pecan Store", "Pé de Caju Bar & Petiscaria", "Caju Bar", "CaJu Lanches e Salgados",
    "Boteco do Juca", "Empório Caju - Cerealista", "Restaurante do Caju", "Lanchonete e Restaurante Caju Verde", "Restaurante Caju Verde",
    "Lanchonete e Restaurante Caju", "Tapiocas e pastéis gourmet do cajú", "Vila Caju", "Lanchonete Nova Skina Caju Verde", "Lanchonete e Restaurante Toca do Caju",
    "Maria Caju", "CAJU MEL DOCES", "Caju açai e lanches", "Atacadão - São Bernardo Centro", "Web Atacados", "Vencedor Atacadista", "Atacado Bem Barato",
    "Assaí Atacado e Varejo", "Mafat atacado de roupas semi novas e variedades", "Tenda Atacado - Diadema", "D&S Atacado e Varejo Infantil", "Grupo Bem Barato",
    "Atacado de folheados", "BRITO & CASONATO Distribuidora de TNT (tecido-nao-tecido)", "Atento atacadista", "Mega Boi", "L Modas Jeans Atacado e Varejo",
    "Utensílios e Utilidades Domésticas Atacado e Varejo Estrela Das Compras", "Carne Atacado", "Formosa Atacado", "Reis Atacado", "J.A modas e Lingeries atacado e varejo",
    "Oba Hortifruti Farm - Mercado, Frutas, Verduras, Legumes, Açougue e Adega", "Hirota Food", "Mercado DuParque ll", "DIA Supermercado", "Extra Mercado",
    "MinhaAmazonBR", "May 13", "Almeida Leme market", "Mercado Lucas", "Mercado Jupiter 1", "Bom Fran Mercado", "Mercado Cico", "Mercado Loyola", "Supermercado Sambelar",
    "Mercado Bom Preço", "Mercado Azevedo", "EMPÓRIO ALEX - SÃO BERNARDO PLAZA SHOPPING", "Empório Prime", "Empório do Amâncio", "Empório Marcon - Padaria em São Bernardo",
    "Empório Eliete", "Restaurante Empório Demarchi no Centro", "EMPÓRIO BLACK BAETA", "Barbecue is the name", "Empório do Miro", "Emporio abadejo", "EMPORIO DO ACO",
    "Empório do Bacalhau", "EmpÓRIO ALEX - SBC - CENTRO", "Emporio Norte Natural", "EmpÓRIO SETE MESTRES", "Empório Esperança", "Empório Uai Berno melhor de Minas SBC",
    "Empório Canaã", "Empório Grand Prime", "Empório EPB", "7cdrinks - Batidas & caipirinhas", "Marula Artesanal Morin - Licor", "Imigrantes Bebidas", "Magazine",
    "Empório Frei Caneca", "Cachaçaria Dalic", "Cachaça é Presente", "Emporio Vignamazzi | Center Norte", "Empório Frades", "Licoretto Bebidas", "Adega Do Alê",
    "Liquore di Famiglia - Licores artesanais", "Drinks distributor Hs", "Mister Bebidas", "Empório Marino , Produtos Importados no ABC", "Adega La Casa das Bebidas",
    "Vilari Empório de Bebidas", "Instituto Baru", "Baru", "Barú Marisquería", "Baru Restobar", "Baru Restaurante", "Baruk Burger Ferrazópoilis SBC", "Baru Imóveis",
    "Lojabaru", "BARU Records", "Baru Learn & Play", "Baru Reforma E Construção", "Baru Surf Br", "Baru Trans Transporte Executivo", "Baru Utilidades e Conveniencias loja virtual",
    "SUCO BAGACO SÃO BERNARDO PLAZA", "Suco Bagaco Shopping ABC", "Suco Bagaço", "Juice station", "Guib's - sucos e pasteis e lanches", "Mister Coco Sucos Naturais",
    "Santo Suco", "Madureira Sucos Itaim Bibi", "Buona Vita", "GoJuice Natural Food", "To 10 Sucos & Lanches", "Pães Doces Sucos Lanches", "Vilajo Sucos e Lanches",
    "Canapum Sucos", "Bom Suco Liberdade", "Restaurante e Lanchonete Nova Geração"
]



# Executa a consulta das empresas
consulta_empresas(empresas)
