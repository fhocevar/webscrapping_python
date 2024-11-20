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
        url = f'https://www.google.com/search?q={nome_empresa_codificado}+Salvador'  # Alterado para Salvador
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
    with open('empresas_Salvador_TEL.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_Salvador.csv com {len(dados_empresas)} registros.")

# Lista de empresas
empresas = [
    "Castanhaê Produtos Naturais",
    "Castanha Produtos Naturais",
    "Castanhas do Nutri",
    "NUTRIGRANEL",
    "Mundo a Granel",
    "Natureza & Cia",
    "Empório Puríssimo",
    "Grãos da Natureza",
    "ATACADÃO DOS GRÃOS",
    "Saúde Total - Produtos Naturais - Suplementos - Pernambués",
    "Tudo Saudável e natural",
    "Mundo das castanhas e mais",
    "Empório Carvalho",
    "Sabor Baiano",
    "Tok Essências e Ervas",
    "Grão",
    "Loja Grão Real",
    "Casa de Produtos Naturais",
    "Natu Ervas",
    "Fruits & Co.",
    "Casa das Baianas",
    "Fazendosca Sabor da Natureza",
    "Nutrimaster Alphaville",
    "Docesfranci",
    "NOZ MOSCATA",
    "Nozes Glacê",
    "Tortaria Macadâmia",
    "Banana Real Sorveteria e Açaiteria",
    "Sr. Banana Açai - Barra",
    "Disk Bananas",
    "Produtos Naturais Empório Gostos da Bahia",
    "Sítio Caju - ANTIGO CT DO ATLÂNTICO",
    "Restaurante Cajueiro",
    "Oficina de Caju",
    "Caju Restaurante",
    "O Caruru",
    "Salvador Atacadista",
    "Atacadão - Salvador Mares",
    "Total Atacado",
    "Atacadão South Center - Distribution Center",
    "Atacadão",
    "Bom Gosto Atacado",
    "Central do Atacado - Salvador",
    "Aline Atacado Salvador",
    "Empório Cidade Jardim",
    "Empório Coisas de Minas Stiep",
    "Emporio Itaigara",
    "Grupo Empório",
    "Empório dos Grãos Salvador",
    "Quinta Avenida Emporio",
    "EMPÓRIO MAGMA",
    "Empório Bahia",
    "Empório Supermix - Imbuí",
    "Empório das Malhas",
    "Mercado Empório",
    "Empório Gradin",
    "Licor da Vó Nieta",
    "Licor da Lai",
    "Mundo do Licor",
    "Licor e Sequilho - Dona Senhora Produtos Artesanais",
    "@licoreira",
    "Campos Brasil Inc.",
    "Casa do Licor Olhos D'ÁGUA",
    "Rc Varietê",
    "Delícias da Dona Glória",
    "BAHIA BEBIDAS - Especialista em Licores",
    "Jota S licores",
    "EMPÓRIO DO ÁLCOOL LD",
    "Licor Dom Gourmet",
    "Depósito Santago",
    "Susanne’s Distribuidora de Licor Roque Pinto",
    "Casa de Licor Mandacaru",
    "NJ Bebidas e Variedades",
    "Casa do Licor - Dona Ivânia",
    "Licor Caseiro",
    "Baru's Pizzaria"
]

# Executa a consulta das empresas
consulta_empresas(empresas)
