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
        url = f'https://www.google.com/search?q={nome_empresa_codificado}+São+Paulo'
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
    with open('empresas_saopaulo.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_saopaulo.csv com {len(dados_empresas)} registros.")

empresas = [
    "Noz do Brasil - Produtos Naturais - Vila Prudente SP", "Empório das Castanhas", "Supermercado Castanha", "Empório Santa Castanha",
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


# Executa a consulta das empresas
consulta_empresas(empresas)
