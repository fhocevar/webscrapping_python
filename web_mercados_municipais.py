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
    chrome_options.add_argument("--headless")  # Para rodar sem interface gráfica
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Função para realizar a consulta e coletar os dados das empresas
def consulta_empresas(empresa_list):
    driver = configurar_navegador()  # Inicializa o navegador
    dados_empresas = []

    for nome_empresa in empresa_list:
        nome_empresa_codificado = quote(nome_empresa)
        url = f'https://www.google.com/search?q={nome_empresa_codificado}'
        driver.get(url)

        try:
            # Coleta o nome
            nome = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h3'))
            ).text.strip()

            # Coleta endereço
            endereco_elementos = driver.find_elements(By.XPATH, '//span[contains(text(),"Endereço") or contains(text(),"Localização")]/parent::div')
            endereco = endereco_elementos[0].text.strip() if endereco_elementos else 'Endereço não disponível'

            # Coleta telefone
            telefone_elementos = driver.find_elements(By.XPATH, '//span[contains(text(),"Telefone") or contains(text(),"+55")]')
            telefone = telefone_elementos[0].text.strip() if telefone_elementos else 'Telefone não disponível'

            # Website
            website_elementos = driver.find_elements(By.XPATH, '//a[contains(@href, "http")]')
            website = website_elementos[0].get_attribute('href') if website_elementos else 'Website não disponível'

            dados_empresas.append([nome, endereco, telefone, website])

        except Exception as e:
            print(f"Erro ao buscar {nome_empresa}: {e}")
            dados_empresas.append([nome_empresa, 'Não encontrado', 'Não encontrado', 'Não encontrado'])

    driver.quit()

    # Salvando os dados em um arquivo CSV
    with open('mercados_municipais_TEL.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)

    print(f"Dados salvos em mercados_municipais_TEL.csv com {len(dados_empresas)} registros.")

# Lista de empresas
empresas = [
    "Mercado Elias Mansour",
    "Mercado Velho",
    "Mercado Municipal Francisco Assis Marinheiro",
    "Mercado Municipal Aziz Abucater",
    "Mercado Municipal 6 de Agosto",
    "Mercado Municipal da Cidade do Povo",
    "Mercado dos Colonos",
    "Mercado Municipal do 15",
    "Mercado Municipal do Bairro São Francisco",
    "Mercado Público do Jacintinho",
    "Mercado da Produção",
    "Mercado Público do Jaraguá",
    "Mercado Municipal",
    "Mercado Central de Macapá",
    "Mercado Municipal Adolpho Lisboa",
    "Mercado Municipal do Morro da Liberdade",
    "Mercado Municipal Walter Rayol",
    "Mercado Municipal da Cachoeirinha",
    "Mercado Municipal Dr. Jorge de Moraes",
    "Mercado Municipal da Glória",
    "Mercado Modelo",
    "Mercado Municipal da Liberdade",
    "Mercado Municipal de Cajazeiras",
    "Mercado Central de Fortaleza",
    "Mercado Central",
    "Mercado Municipal de Vitória",
    "Mercado Central de Goiânia",
    "Mercado Municipal de São Luís",
    "Mercado do São Francisco",
    "Mercadão Municipal Campo Grande"
]

# Executa a consulta
consulta_empresas(empresas)
