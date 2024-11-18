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
        time.sleep(3)  # Aguarda o carregamento da página

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
    with open('empresas130_testando3.csv', mode='w', newline='', encoding='utf-8') as file:
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
    "Mundo dos Grãos", "Distribuidora Viva Alimentos Naturais", "Simples & Natural - Grãos e Castanhas", "Nutty Bavarian", "Nutty Bavarian",
    "Noz do Brasil - Produtos Naturais - Vila Prudente SP", "Nutty Bavarian", "Nutty Up", "Empório das Castanhas", "M.J. Doces E Castanhas",
    "Supermercado Castanha", "Mercadão Natural", "Empório das Castanhas", "Pedro das Castanhas", "Empório Zanata", "Nutty Bavarian",
    "Empório Santa Castanha", "Brazilian Nuts - Açaí, sucos e castanhas - Vila Madalena, São Paulo", "Armazém Paes e Paes Zona Cerealista do ABC",
    "Nutty Bavarian", "EMPÓRIO SETE MESTRES", "Nutty Bavarian", "Noz do Brasil - Produtos Naturais - Vila Prudente SP", "Macadâmia Cerealista LTDA",
    "MACADÂMIA MERCADO SAUDÁVEL", "Macadamia Bolsas e Acessórios", "Macadâmia Home", "Macadâmia moda feminina", "Mr. Cheney - Cookies",
    "Biscoitê A Biscoiteira", "Dadiva Natural - Loja de Produtos Naturais Santo André", "Macadâmia Bela Vista", "Restaurante Bananeira",
    "Pecan Restaurante - Shop. Paineiras", "Residencial Pecan", "Pecan Móveis Planejados", "Loteamento Fechado Pecan (Lotes a partir de 360 M2)",
    "Pecan Store", "Caju", "Pé de Caju Bar & Petiscaria", "Caju Bar", "CaJu Lanches e Salgados", "Boteco do Juca", "Caju", "Empório Caju - Cerealista",
    "Restaurante do Caju", "Lanchonete e Restaurante Caju Verde", "Restaurante Caju Verde", "Lanchonete e Restaurante Caju", "Tapiocas e pastéis gourmet do cajú",
    "Caju", "Vila Caju", "Lanchonete Nova Skina Caju Verde", "Lanchonete e Restaurante Toca do Caju", "Maria Caju", "Caju Bar", "CAJU MEL DOCES",
    "Caju açai e lanches", "Atacadão - São Bernardo Centro", "Vencedor Atacadista", "Assaí Atacado e Varejo", "Assaí Atacadista", "Atacado Bem Barato",
    "Tenda Atacado - Diadema", "Atento atacadista", "Grupo Bem Barato", "Oba Hortifruti Farm - Mercado, Frutas, Verduras, Legumes, Açougue e Adega",
    "Atacado de folheados", "Mega Boi", "Choco Art Artigos Para Festas/ distribuidora / doces / confeitaria /atacado / varejo / essências / artesanato / bisqui",
    "Mafat atacado de roupas semi novas e variedades", "Coco Atacado E Varejo", "L Modas Jeans Atacado e Varejo", "Suplemercado FIT supplements São Bernardo Wholesale & Retail",
    "La Bella Semijóias - Atacado de Semijóias", "Nova Veneza - Atacado e Varejo", "Brasileirão Atacado", "Grupo Bem Barato", "Oba Hortifruti Farm - Mercado, Frutas, Verduras, Legumes, Açougue e Adega",
    "Mercado Vila Nova", "Grupo Bem Barato", "Mercado RV", "Mercado Loyola", "Mercado DuParque ll", "Extra Mercado", "Mercado Lucas", "May 13",
    "Mercado Cico", "Extra Mercado", "Mercado Azevedo", "Hirota Food", "DIA Supermercado", "Vencedor Atacadista", "Bom Fran Mercado",
    "SuperFoods Brasil", "Natural da Terra", "Fispal Food Service", "Naturaltech", "B2Brazil", "Bio Mundo", "Arezzo Alimentos",
    "Grãos e Cia", "Mercado Brasil Natural", "Natural One", "Viver Melhor", "Vila Granel", "Kopenhagen", "Cacau Show", "Nestlé",
    "Vovó Benta", "Olist", "Etsy Brasil", "Consultoria Food Network", "ProFood Consulting", "Griletto", "Giraffas", "Burger King",
    "Nuts & Seeds Trading", "Global Nuts Trading", "Brazil Nuts Export", "Spasso Natural", "Prana Store", "Biospirit", "Empório da Papinha",
    "Yoki Alimentos", "Camil Alimentos", "Polo Distribuidor", "Mega Atacado", "Ketra Alimentos", "Distribuidora GSC"
]


# Executa a consulta das empresas
consulta_empresas(empresas)
