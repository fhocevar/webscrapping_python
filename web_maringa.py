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
        url = f'https://www.google.com/search?q={nome_empresa_codificado}+maringa'  # Alterado para Campinas
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
    with open('empresas_maringa_TEL.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_maringa_TEL.csv com {len(dados_empresas)} registros.")

# Lista de empresas em maringa

empresas = [
    "DIVINA CASTANHA",
    "Nutty Bavarian Maringa",
    "Dica Natural Produtos Naturais",
    "Nutty Bavarian Castanhas Glaceadas Shopping Maringa Park",
    "Armazém dos Anjos Produtos Naturais",
    "Empório & Cia Produtos Naturais - Loja Duque",
    "Armazém Da Nutri",
    "Nutribom Food Shop",
    "Armazém Saúde & Vida - Produtos Naturais - Maringa",
    "Casa Verde - Produtos Naturais",
    "Semprebom Natural Products",
    "Emporio do Ingá Produtos Naturais",
    "palmeriano brasil",
    "Armazém Vida Saudável Produtos Naturais",
    "Empório Santa Cruz",
    "Empório & Cia Produtos Naturais - Loja Paraná",
    "Vila Verde - Empório Natural",
    "Temperos & Saúde Produtos Naturais",
    "INGÁ NUTS",
    "Genevitta Mercado e Restaurante - Carlos Borges",
    "Nutty Bavarian Maringa",
    "CAR CLUB NOZES",
    "Banana Com Aveia - Produtos Naturais",
    "Banana Doce",
    "Bananas Schimitt",
    "Comércio de Bananas Santomé - Maringá",
    "Banana",
    "Cestas Doce & Cacau Maringá",
    "Coco Bambu Maringá",
    "Cacau Show",
    "Cacau Show Angeloni",
    "Santo Bar",
    "Brasil Cacau",
    "Doces Cacau Ateliê Café - Maringá",
    "Cacau Show - Revenda Doce Cacau",
    "Brazil Cocoa Chocolates",
    "Cacau Cordeiro",
    "Cacau Show - Chocolates",
    "Doce du Cacau",
    "Cacau Braga",
    "Natureba Bistrô",
    "Atacado Maringá",
    "Atacadão - Maringá Fernão Dias",
    "Muffato Max Wholesaler",
    "Shopping Vest Sul | Atacado de Moda",
    "Atacadão - Maringá Colombo",
    "Atacadão Maringá",
    "Assaí Atacadista",
    "Bem Bom ATACADISTA",
    "Master Atacado",
    "Vale Atacado",
    "VemKiTem Atacarejo Maringá",
    "Paraná Moda Park Shopping Atacadista",
    "Atacadão da Indústria Melhor e Maior Loja de EPI e Uniformes em Maringá e Sarandi Distribuidor Para Todo Território Nacional",
    "Miss Store Maringá - Atacado e Varejo",
    "Distribuidora Miranda Ltda",
    "Leonardo Comércio Atacadista",
    "Jhonny Atacado",
    "Camilo Atacadista",
    "Mercadão of Maringa",
    "Supermercado Condor Maringá",
    "Super Muffato Maringá - João Paulino",
    "Supermarket Angeloni Maringa",
    "Mercado Municipal",
    "Super Muffato Maringá - Avenida São Paulo",
    "Amigão Supermercados - Tamandaré",
    "Borba Gato market",
    "Cidade Canção Supermarkets - Tuiuti",
    "Amigão Supermercados - Nildo Ribeiro",
    "Empório da Cerveja - Maringá",
    "Empório Sorrechi",
    "Empório Reis",
    "Empório Dudê | Hortifrúti e Mercado Delivery e Loja Física",
    "Empório Marques",
    "Casa Guermandi - Empório de Queijos, Cestas e Presentes",
    "Empório Gourmet confeitaria, cafeteria e bolos artesanais",
    "EMPORIO DOS NATURAIS - Maringa ( EMPORIODOSNATURAISMGA)",
    "Empório Maringá",
    "Empório São José - Produtos Mineiros e Nordestinos"
]


# Executa a consulta das empresas
consulta_empresas(empresas)
