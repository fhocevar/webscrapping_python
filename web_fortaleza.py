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
        url = f'https://www.google.com/search?q={nome_empresa_codificado}+fortaleza'  # Alterado para Fortaleza
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
    with open('empresas_fortaleza.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_fortaleza.csv com {len(dados_empresas)} registros.")

# Lista de empresas em Fortaleza
empresas = [
    "Empório Natural Fortaleza",
    "Casa Saudável Fortaleza",
    "Nutri Vida Produtos Naturais Fortaleza",
    "Grão & Cia Fortaleza",
    "Mercadão Natural Fortaleza",
    "Casa da Castanha",
    "Esquina da Castanha",
    "Cajuzinho",
    "Mega Nuts",
    "Aleison Castanhas",
    "Castanha Quixadá",
    "Castanhas Carlos Veras",
    "Recanto das Castanhas",
    "Castanhas e Redes Ceará",
    "J&A Castanhas",
    "Eudes Castanhas e Doces",
    "J.AQUINO",
    "CASTANHAS VILAMAR",
    "Castanha do Madalena",
    "Cosmo O Rei Da Castanha",
    "Castanhas da Fran",
    "MS Castanhas",
    "Castanha do Aleison",
    "Fábio Castanhas",
    "Resibras Industria Ltda Chestnuts",
    "Banana Passa Natbana",
    "Caju Restaurante",
    "Doce Caju Brasil",
    "Cajú Pratas",
    "Loja Casnutri",
    "Caju Cria Arquitetura",
    "Caju Budega",
    "Cajuí Castanhas",
    "Caju car reboque",
    "CajuBelly",
    "Instituto Caju Brasil",
    "Caju Bar",
    "Cajuplast",
    "Caju Leste",
    "Atacadão - Fortaleza Vila Peri",
    "Mega Atacadista",
    "Atacado direto da fábrica",
    "Atacadão Mix",
    "Atacadão - Fortaleza BR 116",
    "Atacadão - Fortaleza Papicu",
    "FÁBRICA DE ROUPAS PLUS SIZE LIKS",
    "Atacadão - Fortaleza Aeroporto",
    "Atacadão - Fortaleza Osório",
    "Loja Miss Anne",
    "Novo Atacadista",
    "Atacadão Dos Plásticos",
    "DLR Jeans",
    "Assaí Atacadista",
    "Sodine Atacado",
    "Taty Mary",
    "Fácil Atacado",
    "Larbos Varejo e Atacado",
    "Laredo Atacado e Varejo",
    "Reino das Pelucias",
    "Mercado Fortaleza",
    "Empório de Fátima Delicatessen",
    "Empório Delitalia",
    "Empório Del Quartiere",
    "Empório Café",
    "Empório do Pão",
    "Empório da Roça",
    "Empório Delice",
    "Empório Flores e Sabores",
    "Empório do Planalto",
    "Empório Hortifruti",
    "Empório do Carmo",
    "Empório Cearense Delicatessen",
    "Emporium - Produtos Naturais e Regionais",
    "Emporio Verona",
    "Empório Brownie",
    "Empório Dalila",
    "Empório da Garrafa",
    "Padaria Nova Empório",
    "Vem de Make",
    "Distribuidora Brasil Bebidas",
    "Crazy Coquetéis",
    "Option Distributor Food and Beverage",
    "Loja da Bebida",
    "ADB DISTRIBUIDORA",
    "Loja da Bebida Sul",
    "Budega Delivery de Bebidas",
    "Brava Wine",
    "Mercadinhos São Luiz",
    "Alambic Bebidas e Conveniência",
    "Casa dos Licores",
    "Órbita Blue",
    "Keruh Bebidas",
    "Lino Licores",
    "Real Sucos",
    "Tropical Sucos",
    "TropiSucos",
    "Apl Laranja e Mania Sucos",
    "Fortal Sucos",
    "Frutas e Da Fruta",
    "LaranJá",
    "Natura Suco",
    "Rainha do Suco"
]


# Executa a consulta das empresas
consulta_empresas(empresas)
