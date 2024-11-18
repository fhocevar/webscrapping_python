from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Configuração do Selenium com o WebDriverManager
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executa sem abrir a janela do navegador
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Usa o WebDriverManager para obter o ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def consulta_empresas_guia(termo_busca):
    url = f'https://www.guiamais.com.br/busca/{termo_busca.replace(" ", "%20")}'
    
    # Inicia o navegador
    driver.get(url)
    time.sleep(3)  # Espera o carregamento da página
    
    # Captura o HTML da página carregada
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Extrai informações
    empresas = []
    for empresa in soup.find_all('div', class_='company-card'):
        nome = empresa.find('h2').text.strip() if empresa.find('h2') else 'Nome não disponível'
        telefone = empresa.find('span', class_='phone').text.strip() if empresa.find('span', class_='phone') else 'Telefone não disponível'
        endereco = empresa.find('span', class_='address').text.strip() if empresa.find('span', 'address') else 'Endereço não disponível'
        empresas.append({'nome': nome, 'telefone': telefone, 'endereco': endereco})

    if not empresas:
        print("Nenhuma empresa encontrada para o termo de busca.")
    
    return empresas

# Exemplo de consulta
termo = "castanhas"
dados_empresas = consulta_empresas_guia(termo)

# Exibe os resultados
for empresa in dados_empresas:
    print(empresa)

# Fecha o navegador
driver.quit()
