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
        url = f'https://www.google.com/search?q={nome_empresa_codificado}+são+goncalo+RJ'  # Alterado para São Gonçalo, RJ
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
    with open('empresas_sao_goncalo_TEL.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_sao_goncalo_TEL.csv com {len(dados_empresas)} registros.")

empresas= [
    "Tyago da Castanha",
    "Vanessa Castanhas",
    "Castanhas Sabor do Piauí",
    "Assaí Atacadista",
    "Mercado Central",
    "Empório do Zeca",
    "Nutty Bavarian - São Gonçalo Shopping",
    "Casas Pedro",
    "MARA CASTANHA",
    "Empório C&B",
    "Casa de Bolos São Gonçalo, RJ",
    "Espaço Gourmet - Peixaria Moderna",
    "The Sao Goncalo",
    "Meraki tortas e salgados",
    "Loja Point da Mari",
    "Atacadão - Manilha",
    "Supermercados Guanabara",
    "Natural Gourmet - Guanabara",
    "Irmãos Da Terra",
    "Cosmétika Carioca",
    "Mundo Verde Carrefour Alcantara",
    "Primus Produtos Naturais",
    "Qamar Lanchonete, Sorvetes e Cafeteria",
    "Perfumaria Kennedy",
    "CEASA",
    "ZÉ GAROTÃO - Produtos para Sorveterias e Confeitarias",
    "D&D Cosméticos",
    "Atacadão - São Gonçalo",
    "Carioca Grãos & temperos",
    "Casas Verde Produtos Naturais",
    "JJDistribuição de suplementos naturais",
    "Gran Maché Mercado",
    "Distribuidora de Bananas Marilúcia",
    "Chiquita Banana",
    "Casa da Banana",
    "São Gonçalo Shopping",
    "Caju",
    "Atacadão Saara",
    "JJ ATACADO",
    "Atacadão of Trailer",
    "Atacado E Varejo",
    "Atacadão Posto 13",
    "Mikro Atacado e Distribuidor - CEASA",
    "Didanda | Moda Feminina | Atacado e Varejo | Plus Size",
    "Atacaderj Ceasa",
    "Florplan Atacadista",
    "Shopping das Fábricas UM76",
    "Picolé Atacado E Varejo",
    "M do Brasil - Atacado e Brinquedos",
    "Atacadão TOP Burguer",
    "Nobreza Atacado e Varejo",
    "Jardel Atacadão",
    "Supermarket John",
    "Publix Paraíso",
    "Supermarkets Grand Marché",
    "Mercado Hawair",
    "Supermarket Porto Velho",
    "Mercado JC",
    "Carrefour Hypermarket Alcantara",
    "Supermarket Noroeste",
    "Supermercado Galo Branco",
    "Empório Vírgula",
    "Empório São Pedro",
    "World of Events",
    "Cheirin Bão",
    "Lojas Competição - São Gonçalo LJ06",
    "Citycol São Gonçalo",
    "Cores de Minas São Gonçalo",
    "Pés & Patas Centro São Gonçalo",
    "pg* ton trailler do São Gonçalo",
    "Empório Embalagens e Festas",
    "1001 Sapatilhas São Gonçalo",
    "Lojas Competição - São Gonçalo LJ05",
    "Cresci e Perdi - São Gonçalo",
    "Armazém das Tintas - São Gonçalo | Pinturas | Cores Personalizadas | Acabamento | Tintas e Acessórios",
    "Lojas Steel Home: Placa, Gesso e Forro em São Gonçalo RJ",
    "Kalunga",
    "Rede Varejão Hortifruti - São Gonçalo | Hortifruti São Gonçalo | Delivery | Loja 2",
    "Global Music Shop - Loja de Instrumentos Musicais em São Gonçalo",
    "Depósito do Serginho",
    "Forte das Bebidas",
    "Embraza Bebidas",
    "Portuga´s Bar",
    "Mané São Gonçalo",
    "Embraza Mercado de Bebidas",
    "Jr Depósito De Bebidas",
    "Lekin Licor",
    "Depósito da Lili",
    "Bar do Yoda"
]


# Executa a consulta das empresas
consulta_empresas(empresas)
