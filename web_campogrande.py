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
        url = f'https://www.google.com/search?q={nome_empresa_codificado}+Campo+Grande'  # Alterado para Campo Grande
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
    with open('empresas_Campo_Grande_TEL.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_Campo_Grande.csv com {len(dados_empresas)} registros.")

# Lista de empresas em Campo Grande
empresas = [
    "Nutty Bavarian - Castanhas Glaceadas e Salgadas", "Castanhas da Lu", "Mistura Nativa Produtos Naturais", 
    "Castanhas delivery", "Pistache Emporium Cereals", "Empório Nattu Saúde", "Emporium Good Living", 
    "Empório Mix Grãos", "Green Souk Mercado Natural Unidade Marquês de Lavradio", "Grain & grain - Emporium Light", 
    "deBaRu Castanhas", "Grãos do Park", "Empório Divino Grão", "Armazém 3 Marias - Produtos Naturais e Suplementos", 
    "Varejāo Fazendão", "Sal da Terra Produtos Naturais", "Saúde em Grãos Comercio de Alimentos LTDA", 
    "Empório Viva Mais", "Bioma Empório Natural", "Bento Grão Armazém", "Confeitaria Quebra Nozes - Doceria", 
    "CASA DUARTINA", "Bananaz Bazar", "Distribuidora de Bananas Pereira Ltda", "Frutaria Eco Banana", 
    "Banana e Toffee", "Grão e Grão Ecomercado Chácara Cachoeira", "Barbearia do Caju", "Acerola E Caju", 
    "Ana Caju", "Atacadão - Campo Grande Av. Costa e Silva", "Atacadão - Campo Grande Coronel Antonino", 
    "Distribuidora do Fort Atacadista Campo Grande", "Fort Atacadista", "Atacadão - Jardim Centenário", 
    "Atacadão - Campo Grande Aeroporto", "Fort Atacadista", "Fort Atacadista", "Assaí Atacadista", "Fort Atacadista", 
    "Fort Atacadista", "Assaí Atacadista", "Fort Atacadista", "Morena Atacadista", "Assaí Atacadista", "Fort Atacadista", 
    "Mercadão Municipal Campo Grande", "Assaí Atacadista", "Pão de Açúcar", "Comper Supermercados", 
    "Comper Supermercados", "Carrefour", "Mercado Barão", "Comper Ypê Center", "Hyper Center Comper Zahran 64", 
    "Hiper Center Tamandaré", "Legal Supermercados", "Comper Supermercados", "Legal Supermercados", 
    "Supermercado Pires - Vila Planalto", "Comper Supermercados", "Comper Rui Barbosa - Shop 34", "Hiper Center Campo Grande", 
    "Supermercado Nunes", "Supermercado Pires Júlio de Castilho", "Supermarket Mister Junior", "Empório Equilíbrio Centro", 
    "Nosso Empório", "Pistache Emporium Cereals", "Grão Santo Empório - Loja de Produtos Naturais", 
    "Emporium Good Living", "Empório Carandá", "Empório Terra Morena", "Emporio Vida Leve", "Empório do Cravo", 
    "Empório da Gleice", "A Moda da Bru Pijamas e Cia", "Empório do Mineiro", "EMPÓRIO EQUILÍBRIO EUCLIDES", 
    "Empório do campo", "Empório Mix Grãos", "Empório Bem Viver - Unidade Mascarenhas", "Emporio da Terra", 
    "Kanto de Minas - Empório e Café", "Grain & grain - Emporium Light", "Armazém 3 Marias - Produtos Naturais e Suplementos", 
    "Coronel Beer | Distribuidora de Bebidas e Conveniência", "CGR BEER", "Santa Festa Conveniência", 
    "Clickbeer São Francisco", "Cachaçaria Cantinho da Cachaça e Licores", "Clickbeer Itanhangá", "Enoteca Decanter", 
    "JP conveniência", "Clickbeer Ceará", "Condado do Vinho", "CT Baru", "Fast Suco", "Suco Bagaço", "Zugo - Sucos Naturais", 
    "Suco Frutao", "SL CASA DE SUCOS E ENERGÉTICOS", "Beto Sucos", "Frutteria - Casa de Sucos", 
    "Casa de Suco e Pastelaria do Japonês", "SUCO BAGAÇO", "Rekanto of Guarana", "Frut' Sucos"
]

# Executa a consulta das empresas
consulta_empresas(empresas)