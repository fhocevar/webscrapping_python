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
        url = f'https://www.google.com/search?q={nome_empresa_codificado}+Belo+Horizonte'  # Alterado para Belo Horizonte
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
    with open('empresas_Belo_Horizonte_TEL.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_Belo_Horizonte.csv com {len(dados_empresas)} registros.")

# Lista de empresas em Belo Horizonte
empresas = [
    "Dona Amazônia - Castanhas & Frutas Secas", "Mercado Central de Belo Horizonte", 
    "Empório Paraíso do Granel | Produtos Naturais | Castanhas", "Ananda Empório Mercado Central BH", 
    "Amontada Castanhas BH", "Império dos Cocos", "Típico Ceará", "Nutty Bavarian Belo Horizonte", 
    "Palácio das Castanhas", "Casa Das Farinhas E Castanhas", "EMPORIO VON RONDON", "Conceito Natural", 
    "Armazém Central - Savassi", "Irmãos Oliveira Castanhas e Condimentos", "Ponto das Castanhas e Grãos", 
    "Loja das Pimentas e das Castanhas", "Sr Caju", "GR Castanhas do Brasil", "Grano In Grano", "Castanhas Prime", 
    "A Casa - Mercado a Granel - Savassi", "Buffet Chá Com Nozes", "Rua Macadâmia - Tirol", 
    "Banana Chips - Moda Feminina Infanto Juvenil", "Ponto do Açaí BH", "Goiás fruit", "Poche BH - Savassi", 
    "Garapão - Betânia", "Açaí Beachs Jacuí", "Apoio Mineiro Floramar", "Supermercados BH", "Padaria Boníssima", 
    "Tudo na Brasa", "Arreda pra Cá Empório!", "Porcão BH", "Supermarket Super Mais", "Supermercado Super Mais - Rua Ponte Nova", 
    "Lojas Empório - Belo Horizonte", "EMPORIO BH", "Emporium - Seu a Granel Preferido", "Empório Nacional", 
    "EMPORIO DA TERRA.COM", "Seu Empório BH", "Empório 1992", "Emporio Nutri - Savassi", "Empório Reis", 
    "DaRoça Empório Mineiro", "Empório Mineiro", "Empório Nobre Sabor", "Empório Sírio Libanês", 
    "Empório do Sabor - Loja de Queijos, Sementes, Massas e Frios", "De-Lá - Aquilo que é de Todo Lugar", 
    "Emporio N.M", "Empório Gourmet Brasileiríssimo", "Empório ki Delícia", "Warehouse and Emporium DU CARMO", 
    "Ronaldo Licores & Cachaças", "Bebidas BH Delivery Ltda", "Licor e Cachaça Cavalgada", "Sucos Detox SanoFit_BH", 
    "A Suqueria - Sucos Naturais, Crepes, Saladas e Tudo Mais", "América Sucos Naturais e Pastéis", "Sucos & Cia", 
    "PAÇAI Sucos e Vitaminas", "Praçaí Juice and Vitamins", "Boca de Suco", "Leco Lanches e Sucos Naturais", 
    "Mega Sucos", "Life Sucos Belo Horizonte", "Néctar da Serra"
]

# Executa a consulta das empresas
consulta_empresas(empresas)
