from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

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
        # Navega para o site
        url = f'https://www.guiamais.com.br/busca/{nome_empresa.replace(" ", "%20")}'
        driver.get(url)
        time.sleep(3)  # Aguarda o carregamento da página
        
        # Coleta os dados da página
        empresas = driver.find_elements(By.CSS_SELECTOR, '.company-card')
        
        for empresa in empresas:
            nome = empresa.find_element(By.CSS_SELECTOR, 'h2').text.strip() if empresa.find_element(By.CSS_SELECTOR, 'h2') else 'Nome não disponível'
            telefone = empresa.find_element(By.CSS_SELECTOR, '.phone').text.strip() if empresa.find_element(By.CSS_SELECTOR, '.phone') else 'Telefone não disponível'
            endereco = empresa.find_element(By.CSS_SELECTOR, '.address').text.strip() if empresa.find_element(By.CSS_SELECTOR, '.address') else 'Endereço não disponível'
            website = 'Website não disponível'  # Exemplo, pois não temos o campo de website na página
            nome_contato = nome  # O nome de contato pode ser o mesmo do nome da empresa
            celular = telefone if telefone and telefone.startswith('+55 9') else 'Celular não disponível'

            dados_empresas.append([nome, endereco, telefone, celular, website, nome_contato])

    driver.quit()  # Fecha o navegador

    # Salvando os dados em um arquivo CSV
    with open('empresas.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website', 'Nome de Contato'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas.csv com {len(dados_empresas)} registros.")

# Exemplo de lista de empresas
empresas = ["castanhas", "nozes", "macadamia", "banana passa", "pecan", "caju", "atacado", "mercado", "emporio", "licor"]
consulta_empresas(empresas)
