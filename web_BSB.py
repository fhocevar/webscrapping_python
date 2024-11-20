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
        url = f'https://www.google.com/search?q={nome_empresa_codificado}+Brasília'  # Alterado para Brasília
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
    with open('empresas_Brasilia_TEL.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_Brasilia.csv com {len(dados_empresas)} registros.")

# Lista de empresas
empresas = [
    "Disk Castanhas Produtos Naturais",
    "Império das Castanhas",
    "Rei das Castanhas",
    "Rei Das Castanhas - O Maior Distribuidor de Castanhas e Cupuaçu do Brasil",
    "Castanhas.Com",
    "Castanha & Cia - Feira dos Importados",
    "Casa Das Castanhas",
    "Castanha & Cia Guará",
    "Atacadão das Castanhas",
    "Nuts Delivery Castanhas e Produtos Naturais",
    "Point Das Castanhas",
    "Diamantes Produtos Naturais",
    "Mr. Nutty - Nuts Glaceadas",
    "Grão da Vida - 411",
    "Nutty Bavarian Park Sul",
    "R R Castanhas & CIA",
    "Adeilson & Juliana Castanhas E Cia",
    "Honório's Castanhas",
    "Barraca de Castanhas da Cristiana",
    "Castor Castanhas",
    "Empório Quebra-Nozes",
    "Chá com Nozes",
    "Noz do Brasil - Produtos Naturais",
    "Noz Delicatessen",
    "Residencial Macadamia",
    "Banana Dallas",
    "Banana Corrente Comércio de Frutas",
    "Preço de Banana",
    "Bananas Brasnica",
    "Bio Mundo Carrefour Sul",
    "Boteco Caju Limão",
    "Caju BSB - Copos e Canecas Personalizados",
    "Caju Canecas e Personalizados",
    "Caju Produtos Naturais",
    "Atacadão - Brasília Norte",
    "Atacadista Super Adega SIA",
    "Assaí Atacadista",
    "Atacadão Dia a Dia - SIA",
    "Melhor Atacadista",
    "DF Atacadista Materiais Elétricos",
    "ULTRABOX Grande Colorado",
    "Base Atacado",
    "ULTRABOX Express Estrutural",
    "Boa Atacadista",
    "Pavilhão do Atacado",
    "M3 Atacadista",
    "China Atacadista",
    "Brasília Atacadista - Materiais Elétricos",
    "Lexbom Atacadista",
    "Big Box Supermercados",
    "Mercado Brasília",
    "Supermercado Mais Perto",
    "Mercado do Setor S",
    "Comper Asa Sul",
    "Supermercado Armazém do Geraldo",
    "Carrefour Bairro Asa Norte II",
    "DONA - Mercado, Hortifruti & Adega",
    "Cerramix Supermarket",
    "Empório BSB",
    "Empório Brasília",
    "Vitália Empório",
    "Emporio Brazil Store",
    "Empório Express DF - Asa Sul",
    "Empório Toque Gourmet",
    "Empório Boechat",
    "EMPÓRIO GOURMET PARANOÁ",
    "Empório DOC Gastrobar",
    "Empório Casa do Rei",
    "Emporium of Cosmetics",
    "Emporium 58",
    "Empório do Trigo",
    "EMPÓRIO DE MINAS",
    "Empório Badauê",
    "Empório Cantinho da Roça | Kit Festa",
    "Empório dos Bichos",
    "VINTAGE BISTRO BRASILIA & CONVENIENCIA",
    "Noroeste Distribuidora de Bebidas",
    "VilaNova Licores e Cachaças",
    "Baruch Casa de Licores",
    "Licores Artesanais da Vovó Loza",
    "Fox Importadora",
    "Adega Total Wine",
    "Enoteca Decanter Brasília",
    "Baru Drinks e Petiscos",
    "EMPÓRIO BARU",
    "Baru Bar"
]

# Executa a consulta das empresas
consulta_empresas(empresas)
