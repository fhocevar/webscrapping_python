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
    with open('empresas_portoalegre.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas.csv com {len(dados_empresas)} registros.")

# Lista de empresas fornecida por você
empresas = [
    "Castanhas Produtos Naturais", "ZMS Produtos Naturais", "Armazém do Granel", "Grão Natural - Produtos à Granel, Naturais e Saudáveis em Porto Alegre",
    "O Engenho - grãos e cereais", "Amendoim v.s Nuts", "Giro Orgânico e Sustentável", "Seleção Natural", "Dao Hé Comércio de Produtos Naturais",
    "The Dutch Stand", "Cristal Super Castanhas", "Produtos Naturais Solo Bueno", "Empório Cia Da Nutrição", "Selecionados Uniagro", "Vida Eterna Produtos Naturais",
    "Macrobiótica Sauer", "Produtos Naturais - Meu Lado Natureba - Assis Brasil", "Banca 12", "Produtos Naturais - Meu Lado Natureba - Azenha",
    "Seleção Natural", "Dao Hé Comércio de Produtos Naturais", "Empório Cia Da Nutrição", "Macrobiótica Sauer", "Nozes Glorinha", "Selecionados Uniagro",
    "Viverdi Loja Natural", "MANOS GRÃOS", "GERAÇÃO SAÚDE", "Nozes Pitol", "Tutti Secchi Produtos Alimentícios", "Macadâmia Eco Gourmet",
    "Banana Verde - Consumo Consciente", "Carrefour Hipermercado", "Transp. e Com. de Bananas Borges Ltda", "Banana Startups", "La Bambina",
    "Bananas Borges", "bananamachinada", "Penitenciária Estadual de Canoas 1 (PECAN 1)", "Complexo Prisional de Canoas", "AAPECAN - Associação de Apoio a Pessoas com Câncer",
    "Instituto Brasileiro de Pecanicultura - IBPE", "Pecan do Sul", "Rua Caju - Petrópolis", "Atacadão", "Atacadão - Sertório", "Atacadão",
    "Atacado Libardi", "Atacado do Xuxa", "Atacadão", "Atacadão - Porto Alegre Humaitá", "Atacado JBS", "Via Atacadista - Porto Alegre", "Atacado J.D.L",
    "Atacadão", "Atacado do Xuxa - Filial Anchieta", "Atacado Simionato - Loja Teresópolis", "Vantajão Atacado", "DG Atacadista", "Atacado do Beto - Atacado e varejo de Doces",
    "Atacado de Confecções Fortsul", "Atacado do Junior", "Atacado Rica", "Atacado Atalaia Porto Alegre", "Porto Alegre Public Market", "Mercado Do Porto",
    "Zaffari", "Supermercado Gecepel", "Zaffari Lima e Silva", "Zaffari Menino Deus", "Supermercado Farol", "Supermarket Pezzi - Erico Verissimo",
    "Zaffari Cristóvão Colombo", "Asun Supermercados Azenha: Frutas, Carnes, Bebidas, Verduras Porto Alegre RS", "Mercado e Açougue Tradição", "Peixaria Japesca - Mercado Público",
    "Brasco Florencio market", "Nacional", "Zaffari", "Center Shop Supermercado", "Supermercado Anuar Pezzi", "Zaffari", "Supermercado Gecepel",
    "Keppler Supermercado", "Empório Brasil", "Emporio 471", "Emporio Natural Lindoia Porto Alegre", "Empório 25 - Rua Uruguai", "Empório Menino Deus",
    "Empório 25 Otávio Rocha", "Empório Três Figueiras", "Empório Marinho", "Public Market", "Emporio Veículos", "Empório Belém", "Emporio Saude Natural",
    "Vê - Empório e Restaurante Vegano", "La Tasse Empório", "Empório da Família Loja de Vinhos e Comida Congelada Porto Alegre", "Wine & Food Emporium - WFE",
    "Diet Emporio - Alimentos & Suplementos", "EMPÓRIO DA TERRA PORTO ALEGRE", "Casa Da Bebida Distribuidora de Bebidas", "Costi Bebidas", "Empório Brasil Bebidas",
    "Porto Bebidas", "Dionisia Vinhobar e Restaurante", "GW Imports", "Depósito Vinhos e Afins", "Adega do Holandês I Banca 38", "Bebidas do Sul - Vinhos e Espumantes",
    "Cachaçaria do Mercado", "Adega Sanguiné"
]




# Executa a consulta das empresas
consulta_empresas(empresas)
