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
        url = f'https://www.google.com/search?q={nome_empresa_codificado}+guarulhos'  # Alterado para Campinas
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
    with open('empresas_guarulhos_TEL.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_guarulhos_TEL.csv com {len(dados_empresas)} registros.")

empresas = [
    "Empório dos Cereais & Integrais",
    "Empório Oliveira - Produtos Naturais Guarulhos-SP",
    "Marina Bonita | Casa do Norte e Cerealista",
    "Atacadão do Natural Guarulhos I",
    "Nutty Bavarian - Internacional",
    "Kalpa Empório",
    "Produtos Naturais e Suplementos em Guarulhos - Empório D' Fibra_GRU",
    "Empório Tradições 2",
    "Nutty Bavarian",
    "Casa do Norte GALVÃO",
    "Empório ponto dos graos",
    "Semente & Raiz",
    "Empório Nação dos Cereais",
    "Vila das Castanhas",
    "T P EMPORIO DE PRODUTOS NATURAIS E REGIONAIS NO JARDIM SÃO JOÃO",
    "Bora lá imports",
    "Mercado Ipanema",
    "Empório Bem Estar Brasil",
    "EMPÓRIO ROSA - ZONA CEREALISTA",
    "Noz do Brasil - Produtos Naturais - Vila Prudente SP",
    "Amor Aos Pedaços",
    "Café maçã",
    "Chocolândia",
    "Empório Macadâmia Lorena",
    "Sam's Club",
    "Fabio Bananas distributor",
    "Residencial Pecan",
    "Cajuran Tudo P Sua Construçāo",
    "CEAG - Central de Abastecimento de Guarulhos",
    "Cacau show bom clima",
    "Brasil Cacau - Internacional Shopping Guarulhos",
    "Cacau Show Bonsucesso Roldão",
    "Brazil Cocoa Chocolates",
    "Max Atacadista Guarulhos",
    "Atacadão Souza",
    "Giga Atacado - Guarulhos",
    "Poupaki Atacadista",
    "Assaí Atacadista",
    "Tent Wholesale - Bonsucesso",
    "Tenda Atacado",
    "Roldão Atacadista",
    "Assaí Atacadista | Guarulhos Pimentas",
    "K&N Atacadista",
    "Mercado Iporanga",
    "Shop supermarket Barbosa 06",
    "Supermercado Suprema",
    "Supermarket Of People",
    "Mercado SS Super Super - Loja 2 Vitória",
    "Carrefour Hypermarket Guarulhos",
    "Barbosa Supermercados 24h - Jardim Gracinda",
    "Supermercado Santa Rita",
    "Extra Mercado",
    "Reilar Supermercados",
    "Carrefour Hipermercado - Guarulhos",
    "Market Fonte Nova Munira",
    "Sonda Supermercados - Vila Rio",
    "Empório Guarulhos",
    "EMPÓRIO BELLA VITA",
    "Empório Nossa Terra Rica",
    "Empório Grão de Ouro",
    "Empório Tradições - Bom Clima",
    "Empório Sardinha",
    "Empório Mori",
    "Vilari Empório de Bebidas",
    "Casa Serrana Vinhos E Licores"
]


# Executa a consulta das empresas
consulta_empresas(empresas)
