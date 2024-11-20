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
        url = f'https://www.google.com/search?q={nome_empresa_codificado}+Manaus'  # Alterado para Belém
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
    with open('empresas_MANAUS_TEL.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_Belem.csv com {len(dados_empresas)} registros.")

# Lista de empresas
# Lista de empresas
empresas = [
    "Fábrica De Castanha",
    "Emporio da Castanha",
    "EMPÓRIO DEMASI - CD",
    "Empório Grãos e Saúde",
    "Empório Fragoso Mercado",
    "Delícias Manauara | Bombons Regionais de Cupuaçu e Castanha",
    "Original Nutts",
    "Dona Marlene Produtos Regionais",
    "Empório Di Grano Djalma Batista",
    "Grains Brazil",
    "House of Peanuts",
    "Nutty Bavarian",
    "Dr Doces & Derivados",
    "Reigionais",
    "Casinha do Regional",
    "Armazém e Empório Adolpho Lisboa",
    "Uarini Grãos Dourados Farinha Ovinha",
    "Maria Dondoca - Padaria Saudável",
    "GRUPO CIEX",
    "Sabores do Campo Empório Produtos Regionais da Amazônia",
    "Noz do Brasil - Produtos Naturais - Vila Prudente SP",
    "Empório Rio Negro - Monte das Oliveiras",
    "Arte di Latte",
    "BANANA CHIPS AMAZONAS",
    "Banana & Cia",
    "Feira Moderna da Banana de Manaus",
    "Atacadão da Banana",
    "Feria da Banana",
    "Ponto Da Banana Frita Na Hora",
    "Vena da Banana",
    "Puesto de Banana El Venezolano",
    "Compra E Venda De Banana",
    "Empório DB Recife",
    "Empório DB - Ephigênio Salles 24hr",
    "Superatacado Coema",
    "Pátio Gourmet - Adrianópolis",
    "Empório DB",
    "Empório P10",
    "Empório Di Grano - Campos Eliseos",
    "Hiper DB Nova Cidade",
    "Armazém Português",
    "Hiper DB Ponta Negra",
    "Atacadão - Manaus Moderna",
    "Pátio Gourmet Pátio Djalma",
    "DB Hypermarket St. Anthony",
    "Pare e Leve",
    "Panorte",
    "Hiper DB",
    "Empório Di Grano Adrianópolis",
    "Empório Di Grano Djalma Batista",
    "Atacadão - Manaus Educando",
    "Sabores da Amazônia (Box do Caju)",
    "CAJU BRASIL by Renata Riatto",
    "CajuIdeas",
    "LAVA JATO DO CAJU",
    "Emporium Rodrigues",
    "Mercado Municipal Adolpho Lisboa",
    "Nova Era Compensa: Supermercado, Hortifruti, Peixes, Carnes em Manaus AM",
    "Vitória Supermercados",
    "Supermercado Veneza",
    "Supermercados CO – Unidade Compensa",
    "Nova Era Torres: Supermercado, Hortifruti, Peixes, Carnes em Manaus AM",
    "Supermercado CO - Unidade CENTRO",
    "Assaí Manaus - Aleixo",
    "Carrefour Hypermarket Manaus Adrianópolis",
    "Emporium Rodrigues",
    "Mercadinho Gustavo - São Raimundo Manaus Amazonas",
    "Carrefour Hypermarket Manaus Ponta Negra",
    "Supermercado Fortaleza",
    "Vitória Supermercados",
    "Floripes Supermarket",
    "Nova Era Compensa Ponte: Supermercado, Hortifruti, Peixes, Carnes em Manaus AM",
    "Supermercado Bastos Petrópolis",
    "Nova Era Silves: Supermercado, Hortifruti, Peixes, Carnes em Manaus AM",
    "Supermercado São Paulo",
    "Supermercados Bastos Praça 14",
    "Emporium Sempre Saudável",
    "Empório Di Grano Djalma Batista",
    "Empório de Produtos Naturais Mundo do Cereal - Manaus",
    "Emporio Bread"
]



# Executa a consulta das empresas
consulta_empresas(empresas)
