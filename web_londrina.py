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
        url = f'https://www.google.com/search?q={nome_empresa_codificado}+londrina'  # Alterado para Campinas
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
    with open('empresas_Londrina_TEL.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_joinville_TEL.csv com {len(dados_empresas)} registros.")

# Lista de empresas em Londrina
empresas = [
    "Empório Paraíso do Granel | Produtos Naturais | Castanhas",
    "Gostinho Da Roça",
    "GR Castanhas do Brasil",
    "Dona Amazônia - Castanhas & Frutas Secas",
    "Castanha Baru Londrina - Padaria e Confeitaria Saudável- Sem glúten",
    "Norteminas - Castanhas Selecionadas",
    "Palácio das Castanhas",
    "Sr Caju",
    "Amontada Castanhas BH",
    "Conceito Natural",
    "Naturalissima - O maior a granel de Santa Luzia",
    "Casa Das Farinhas E Castanhas",
    "EMPORIO VON RONDON",
    "Irmãos Oliveira Castanhas e Condimentos",
    "Armazém 50 - Empório Natural - Centro",
    "Loja das Pimentas e das Castanhas",
    "Império dos Cocos",
    "Empório De Grão em Grão",
    "Ébenezer condimentos",
    "Ponto das castanhas e grãos",
    "N.O.Z | Produtos Naturais e Cafeteria Saudável | Londrina",
    "Brasil Cacau",
    "Atacadão - Londrina Ceasa",
    "Atlântico Atacado",
    "Dz Atacado",
    "Super Muffato Tiradentes",
    "Atacado e varejo estilo livre",
    "Atacadão - Londrina Tiradentes",
    "Sabor e Segredo Sex Shop",
    "Ativa Atacado",
    "Atacarejo Paranaíba - ASTECA",
    "Supermercado Super Hora - Jardim Califórnia",
    "ML Mercado",
    "Amigão Supermercados - Londrina Zona Norte",
    "Mercado das Américas",
    "MERCADO STICANELLA",
    "Mercado",
    "Moreira Mercado",
    "Condor Hypermarket",
    "Mercado Decolores",
    "Mercado Igapó",
    "Mercado Edi",
    "Supermarket Real Penta",
    "Mercado JPE",
    "Mercado Bom Preco",
    "Supermercado Maffei",
    "Mercado Caetano",
    "Lynx Market - Bakery From Jorginho",
    "Super Mercado Gomes",
    "Maior MiniMercado",
    "Mercado Pereira",
    "Emporio de Minas",
    "Empório Guimarães",
    "LONDRI BEER - Distribuidora de Bebidas",
    "Licores Alessandro Saba",
    "London Beer",
    "LONDRI BEER",
    "Baru Confeitaria Criativa",
    "Mega Suco",
    "Orgânicos Paraíso",
    "Nattu Orgânico",
    "Orgânicos Shingo",
    "Nature Nutri",
    "Catedral Produtos Naturais - Clube do Natural",
    "OZONTECK LONDRINA",
    "Granarium",
    "Origens Rurais",
    "Atlântica Natural",
    "Amigos Orgânicos",
    "Feira Orgânica de Londrina",
    "Lava Jato & Troca de Óleo Cristal"
]

# Executa a consulta das empresas
consulta_empresas(empresas)
