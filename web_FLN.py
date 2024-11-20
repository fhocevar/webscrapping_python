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
    with open('empresas_FLN.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_saopaulo.csv com {len(dados_empresas)} registros.")

empresas = [
    "Sintonia da Saúde Produtos Naturais", 
    "Loja de Produtos Naturais IMBUR | Casa de Produtos Naturais Florianópolis, Suplementos & Castanhas", 
    "Nutty Bavarian", 
    "Albanos Naturais, Granel e Suplementos", 
    "Nut Store", 
    "Vivenda dos Grãos", 
    "Nutty Bavarian", 
    "Kendra Castanha", 
    "Maria Nuts Produtos Naturais e Alimentação Saudável", 
    "Cia das Fibras - Produtos Saudáveis", 
    "Simples e Natural Armazém Campeche", 
    "DNA Empório Shopping Villa Romana", 
    "Terra Astral Produtos Naturais", 
    "Amazônia Nativa Produtos Naturais", 
    "Diego Produtos Naturais", 
    "Empório Döll - Produtos Naturais", 
    "Maria Nuts Produtos Naturais e Alimentação Saudável", 
    "Macadâmia Bolsas", 
    "Banana Fit Gourmet", 
    "Banana Bacana", 
    "Vanna Banana | Uniformes Criativos Ltda", 
    "Banana Beach Sucos", 
    "Morro do Caju", 
    "CÍLIOS CAJU | LAGOA DA CONCEIÇÃO, FLORIANÓPOLIS", 
    "Com Caju", 
    "Caju Estúdio Criativo", 
    "Pousada Caju Rosa", 
    "Atacadão - Florianópolis JK", 
    "Atacadão - Florianópolis Via Expressa", 
    "Brasil Atacadista", 
    "Fort Atacadista", 
    "Atacado Catarinense", 
    "Atacado Vitória", 
    "Fort Atacadista", 
    "Fort Atacadista", 
    "Brasil Atacadista", 
    "Atacado Litoral", 
    "Fort", 
    "Komprão Koch Atacadista", 
    "ATACADO CATARINENSE", 
    "atacadista", 
    "Angeloni", 
    "Precito Atacado e Varejo de Bebidas", 
    "TLL Atacadista", 
    "YIHAO ATACADO", 
    "Kremer Atacado", 
    "Atacarejo Bebidas", 
    "Mercado Público de Florianópolis", 
    "Angeloni Supermercado", 
    "Angeloni Santa Monica", 
    "HiperBom Supermercados", 
    "Supermercados Imperatriz - Centro Florianópolis", 
    "Angeloni Capoeiras", 
    "Mercado Floripa", 
    "Mercado Taviana | João Paulo - Florianópolis, SC", 
    "Hippo", 
    "Market St George", 
    "Angeloni Supermarket Beira Mar", 
    "Angeloni", 
    "Mercado União", 
    "Bistek", 
    "Mercado Carvoeira", 
    "Supermercado Floripa", 
    "MARKET GUGA EXPRESS", 
    "Carrefour Hypermarket", 
    "Angeloni Bocaiúva", 
    "Imperatriz Supermarket", 
    "Empório Floripa", 
    "Empórium Bocaiuva", 
    "EMPORIO SUL FLORIPA", 
    "Empório Mania da Ilha", 
    "Empório Döll - Produtos Naturais", 
    "Floripa Emporio Gourmet", 
    "Capella Coffee Emporium", 
    "Empório Santa Mônica", 
    "Empório dos Varais", 
    "Empório dos Uniformes", 
    "Empório São Queijo", 
    "Empório Ilha Café", 
    "Marama Produtos artesanais", 
    "Grão & Pronto Healthy food", 
    "Japan Foods Oriental Emporium", 
    "Empório 84", 
    "Emporio Catarinense", 
    "Nut Store", 
    "Supermercados Imperatriz - Centro Florianópolis", 
    "RECK BEBIDAS", 
    "Cachaçaria Quiridhuz", 
    "Liquor Store Brasil - Conveniência", 
    "Office of Liquor", 
    "do Brasil bebidas", 
    "Essen Vinhos Finos", 
    "Levin - Vinhos, empório e presentes", 
    "Onça Bêbada", 
    "Enoteca Decanter Florianópolis", 
    "Trink Bier CHOPP DELIVERY EVENTOS", 
    "Espaço Prime Bebidas - Loja", 
    "Delosantos bebidas", 
    "DARK EMPORIO DE BEBIDAS LTDA", 
    "Licor Cachaça Balneário Camboriú Especial Bebida Destilados Alambique Engenho Don Vico", 
    "Top Market Floripa", 
    "Loja De Bebidas On - Conveniência, Bebida Gelada, Carvão, Gelo", 
    "Chopp Gus", 
    "Piccola Bottega Italiana", 
    "Cachaçaria Schmitz - Cachaça Schmitz", 
    "Baruc Natural", 
    "Le Barbaron", 
    "Balbúrdia Cervejeira Florianópolis", 
    "Le Pario Bistro", 
    "Baogui"
]


# Executa a consulta das empresas
consulta_empresas(empresas)
