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
        url = f'https://www.google.com/search?q={nome_empresa_codificado}+Rio+de+Janeiro'  # Alterado para Rio de Janeiro
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
    with open('empresas_RJ.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_RJ.csv com {len(dados_empresas)} registros.")

empresas = [
    "Nossa Castanha",
    "Trilha Alimentos",
    "Distribuidora - Castanhas do Ciro",
    "Caminho Bem Estar",
    "MARA CASTANHA",
    "FRUTOS DO BRASIL",
    "Nutty Bavarian",
    "Castor Mercado Saudável - Ipanema",
    "Casa Verdini - Suplementos e Produtos Naturais",
    "Zé da Castanha",
    "Nutty Bavarian",
    "Nutty Bavarian - Plaza Niterói",
    "Nutty Bavarian",
    "Nutty Bavarian",
    "Carioca Zen Produtos Naturais",
    "Space Nutcracker",
    "Nutty Bavarian",
    "Noz do Brasil - Produtos Naturais - Vila Prudente SP",
    "Confeitaria Manon Ouvidor",
    "Nutty Bavarian",
    "Macadame Construtora",
    "Rainha da Macadâmia",
    "Banana Br",
    "Pecan Gourmet",
    "Caju",
    "Atacadão Rj",
    "Magui Atacado",
    "Atacadão da Central",
    "Atacadão Carioca",
    "Atacadão Da Brasil",
    "Assaí Atacadista",
    "Chinatown Wholesale and Retail",
    "Lin Atacadão",
    "Assaí Atacadista",
    "Atacado Master",
    "Atacadão do Meier",
    "Rio10 Atacado",
    "Dally Boy Atacadão e Varejo",
    "Sun of the Sahara",
    "Atacado E Varejo",
    "Plus Atacadista",
    "Barracuda Atacado e Varejo",
    "Joeri Atacadão",
    "Impocenter",
    "ATACADÃO BIJU",
    "Municipal Market RJ - CADEG",
    "Rede Big Market",
    "Mercado Popular Uruguaiana",
    "Extra Mercado",
    "Carrefour",
    "Supermercados Mundial Bairro de Fátima | Riachuelo",
    "Mundial",
    "Supermarket",
    "Extra Mercado",
    "Pão de Açúcar",
    "Supermercados Guanabara",
    "Supermarket",
    "Zona Sul Supermercado Largo do Machado",
    "Mercado Imperial do Cosme Velho",
    "Zona Sul Supermercado Barra da Tijuca - Barra Square",
    "Extra Mercado",
    "Supermercados Mundial Praça da Bandeira | Matoso",
    "Zona Sul Supermarket",
    "Supermercados Mundial Botafogo",
    "Extra Supermarket",
    "Lojas Empório - Rua do Ouvidor",
    "Lojas Empório - Copacabana",
    "Empório CR",
    "Empório Gourmet",
    "Empório 37",
    "Empório Lamego",
    "Empório Jardim na Praia",
    "Empório Chic - Bebidas e Snacks",
    "Rio Emporium Cachaçaria",
    "Empório Saúde - Ipanema",
    "Empório",
    "Livraria Saraiva",
    "Empório Rio São Paulo",
    "Empório dos Astros",
    "Empório Vin - Loja de Vinho no Rio de Janeiro",
    "EMPÓRIO YUDI Alimentos e Artigos Orientais",
    "Empório Irmãs da Terra",
    "Emporio Boutique",
    "Empório K",
    "Empório Carioca",
    "Bistrô Empório Rocco",
    "Clovispinga",
    "Deu la deu vinhos",
    "Safra Wine Store",
    "Portal Copa Depósito de Bebidas",
    "CASA BRASIL VINHOS",
    "A Garrafeira",
    "Espírito do Vinho",
    "Planeta Sonho Delicatessen",
    "Bebida In Box Shopping Uptown Barra",
    "Licor Doce",
    "Ocam Vinhos",
    "Planeta Sonho Delicatessen",
    "Porto Di Vino",
    "Koala Conveniencia",
    "Farinha Pura Emporium",
    "Gaspar Cachaçaria",
    "Vino Ipanema",
    "Gullo Tabacaria Tijuca",
    "Vino! Flamengo Wine Bar",
    "Baru Rio",
    "Baru Offshore Navegação Ltda.",
    "Rei dos Sucos",
    "Golden Sucos",
    "Cia dos Sucos",
    "Bibi Sucos",
    "Campeão dos Sucos"
]



# Executa a consulta das empresas
consulta_empresas(empresas)
