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
        url = f'https://www.google.com/search?q={nome_empresa_codificado}+Goiania'  # Alterado para Goiânia
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
    with open('empresas_Goiania_TEL.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_Goiania.csv com {len(dados_empresas)} registros.")

# Lista de empresas em Goiânia
empresas = [
    "Capital Castanhas", "Tropical Castanhas", "JBR Castanhas - Atacadista de Produtos Naturais", "MAISA CASTANHAS", 
    "Terra Santa Castanhas", "Casa Grande Produtos Naturais", "Produtos Naturais - BelaNutri", "Castanhas Favorita", 
    "Anis Produtos Naturais e Especiarias", "Estação das Castanhas", "Empório Casa de Oliva", "Manda Castanha", 
    "RBF CASTANHAS", "Noz Produtos Naturais", "quebra nozes calçados infanto-juvenis", "Noz Produtos Naturais - Buena Vista Shopping", 
    "Macadamia fashion", "Banana Vegana", "Banana Blue", "Distribuidora de bananas Topazil", "Banana Shopping", 
    "Restaurante Outback Steakhouse", "Caju Moda", "Caju Moda Feminina I 44 Goiânia", "Caju Turismo", "Cajueiro - Centro de Juventude", 
    "caju confeitaria", "Lança Caju", "chuva do caju", "Caju Vitta", "Arena Caju", "Cajueiro Bar & Restaurante", 
    "Agropecuária Caju Assessoria e Serviços", "Centro Cultural Cara Vídeo", "Praça Caju Amigo", "Caju pastel", 
    "Atacadão - Goiânia Av. Independência", "Assaí Atacadista", "Atacadista Real Aviamentos", "Rua 44 Goiânia", 
    "GIGANTAO ATACADO E VAREJO", "Master Atacadista", "Prime Atacado Moda Feminina", "UNIVERSO ATACADO E VAREJO", 
    "ROUPAS ATACADO", "Skala Atacadista de Moda", "DaddyCool - Atacado Goiânia", "Universo Store Atacado", 
    "Atacadão Goiano", "Moda Feminina Atacado - Revenda e Lucre", "Mega Stock Atacado", "Ipê Atakarejo", 
    "Campinas Atacado", "Casa Da Mussarela Atacado", "Batista Atacadão", "Mercado Central de Goiânia", 
    "Popular Market of 74", "Campinas Market", "Supermercado Leve", "Supermercado Goiás", "Supermercado Goiânia", 
    "Supermercado Tatico - Centro", "Supermercado Tatico - Campinas", "Bretas Supermercado", 
    "Supermercados Pró Brazilian- Vila Nova", "Supermarkets Pro - Brazilian", "Bretas Supermercado - Anhanguera", 
    "Supermercado Tatico", "Hiper Moreira", "Supermercado Casa Juazeiro", "Super Barão Supermercados - Marista", 
    "Supermercado Prátiko Universitário", "Rede Store – Campinas", "Empório Veccino", "Empório Prime", 
    "Empório Ponto Com", "Empório Philadelphia", "Empório Piquiras - Flamboyant", "Empório Du Carmo — Queijos & Vinhos", 
    "Empório Confrades", "Empório Franciscano", "Empório Madrid - Adega de Vinhos e Distribuidora de Bebidas", 
    "Emporium Syrian Lebanese", "Empório Enquanto isso em Goiás", "Empório Trás-os-Montes", "Goiabão Empório", 
    "Lá de Minas Empório", "Empório Di Goiás", "Empório Alto da Glória", "Emporio Leste", "Empório Dos Pães Goiânia", 
    "LICORES PIERRE", "Empório Mundo das Bebidas veredas buritis", "Noleto Licores", "Parada 21 Bebidas & Presentes", 
    "Cachaçaria do Parente", "Empório Sete - Vinhos Importados e Bebidas em Geral", "Capital Drink empório"
]

# Executa a consulta das empresas
consulta_empresas(empresas)
