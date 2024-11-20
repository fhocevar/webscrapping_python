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
        url = f'https://www.google.com/search?q={nome_empresa_codificado}+campinas'  # Alterado para Campinas
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
    with open('empresas_campinas_TEL.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_campinas_TEL.csv com {len(dados_empresas)} registros.")

# Lista de empresas em Campinas
empresas = [
    "Empório Natural Campinas",
    "Casa Saudável Campinas",
    "Nutri Vida Produtos Naturais Campinas",
    "Grão & Cia Campinas",
    "Mercadão Natural Campinas",
    "Casa da Castanha Campinas",
    "Esquina da Castanha Campinas",
    "Cajuzinho Campinas",
    "Mega Nuts Campinas",
    "Casa das Castanhas",
    "Mania de Castanha",
    "Empório Delícia a Granel",
    "Armazém Nativa",
    "Grãos do Castelo",
    "Empório do Parque",
    "Barão Ervas - Saúde com Natureza Produtos Naturais",
    "Casa Rosa Produtos Naturais Granel",
    "Armazém Barão Hortifruti",
    "Empório Integrale",
    "Nutty Bavarian",
    "Quero Grão Produtos Naturais",
    "M Castanha Precatórios",
    "AFUÁ GRÃOS",
    "Sabor Brasileiro Drageados",
    "Produtos Naturais - Granel, Marmitas Fit, Suplementos",
    "Mister Nuts",
    "Casa das Ervas",
    "Casa Naturale",
    "Cantinho Coisa Nossa",
    "Cha Com Nozes Propaganda",
    "Macadâmia Bela Vista",
    "QueenNut Macadamia",
    "Sonho de Verão",
    "Banana Café",
    "Bananas Nacional",
    "Lagundri Campinas",
    "Pecan Restaurante - Shop. Paineiras",
    "Caju Moda Feminina",
    "Caju Flor Ateliê",
    "Menu do Caju",
    "Chocolate da Caju",
    "Atacadão - Campinas Dom Pedro",
    "Higa Atacado",
    "Assaí Atacadista",
    "Makro - Shop Santos Dumont",
    "Max Atacadista",
    "DG Atacado",
    "Tenda Atacado - Campinas Ceasa",
    "Giga Atacado - Campinas",
    "Roldão Atacadista",
    "Campinas Market",
    "Savegnago Supermercados",
    "Supermercado Taquaral",
    "Vila Mais Supermercados",
    "Mercado Princesa",
    "Mercado Riachuelo",
    "Galassi",
    "Empório Santa Therezinha",
    "EMPÓRIO BELLÍSSIMO",
    "Empório D'Abolição",
    "Excelência Vinhos",
    "Adega Da Familia",
    "Grand Cru Campinas",
    "Empório Taquaral",
    "Nono Bier",
    "Miami Store",
    "Decanter Campinas Gramado Mall",
    "Vila Prado Empório",
    "O Senhor dos Licores",
    "Baru Restaurante",
    "Sabor da Fruta",
    "Casa de Sucos Batidão Campinas",
    "Suco de Praia",
    "Império do Suco",
    "Sucão - Centro Campinas",
    "Suco Bagaço",
    "Sucão Cambuí"
]

# Executa a consulta das empresas
consulta_empresas(empresas)
