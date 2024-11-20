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
        url = f'https://www.google.com/search?q={nome_empresa_codificado}+maceio'  # Alterado para Campinas
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
    with open('empresas_maceio_TEL.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_maceio_TEL.csv com {len(dados_empresas)} registros.")

empresas = [
    "Império das Castanhas",
    "Bodega da Castanha",
    "Sabor Maceió",
    "Cajual Produtos Nordestinos",
    "VIVA + CAJÚ - CASTANHAS",
    "Casa Nordeste Pajuçara",
    "O Baiano",
    "Limaalimentos fábiano das castanhas",
    "LIAO CASTANHAS",
    "Armazém Anandda",
    "Mercado Verde Alimentos Saudáveis",
    "Gelato Borelli Maceió",
    "Sam's Club Maceió",
    "Mundo Verde",
    "LEVE DIET GOURMET",
    "Jb Passa",
    "Caju.ateliê",
    "Praça Sandoval Cajú",
    "Recanto do Cajueiro",
    "Carne de Caju Delícias",
    "Caju Ameixa",
    "Chocolate Brasil Cacau",
    "Ponto do Açaí",
    "Casa Nordeste",
    "Cookie Cakau",
    "Cacau Show",
    "Império das Castanhas",
    "Casa Nordeste Pajuçara",
    "Cacau Show Sam's Club",
    "Cacau Especial",
    "Bodega da Castanha",
    "Cacau Show - Chocolates",
    "Cacau Show",
    "Atacadão - Maceió Aeroporto",
    "Super Atacado - Antares",
    "Atacadão Boa Vista",
    "Big Atacado",
    "Atacadão - Maceió",
    "Atacadão - Maceió Petrópolis",
    "Assaí",
    "Dmais Atacado e Varejo",
    "Assaí Atacadista",
    "PH Atacado",
    "Assaí Atacadista",
    "ATACADÃO FEITOSA",
    "Assaí Atacadista",
    "Alforria Atacado",
    "Atacado Maceió",
    "Atacadão dos Kits Maceió",
    "Felicidade Distribuidor Atacadista",
    "NL ATACADOS",
    "Atacadão do Jeans ADJ - Loja 3",
    "Atacadão Boa Vista",
    "Mercado Popular",
    "Mercado da Produção",
    "MERCADO PÚBLICO",
    "Peixaria Peixe Dourado",
    "Mercado Público do Jacintinho",
    "Mercado do Artesanato",
    "Palato",
    "UniCompra",
    "UniCompra",
    "Emporio nordestino",
    "Mercado das Artes 31",
    "Mercado da Feirinha do Jacintinho",
    "Mini Market Pajuçara",
    "Mercado da Gruta",
    "UniCompra",
    "District Flower",
    "Mercadinho Alagoiás",
    "Supermercado Mega Marx Feitosa",
    "G supermercado",
    "José Francisco dos Santos Mercado",
    "Empório Maceió",
    "Empório Farol",
    "Emporio nordestino",
    "Empório Colina Maceió",
    "Empório Top | Loja de Roupas e Acessórios Masculinos em Maceió",
    "Empório Millano - Vinhos, Massas, Risotos, Tábuas de Frios",
    "Empório Panificação",
    "Empório La Zuka",
    "EMPORIO R > MODA FEMININA",
    "Empório Ariel",
    "Estilo Empório",
    "Empório Do Sertão Frios & Laticínios",
    "Emporium bread",
    "Empório Pizzaria",
    "Empório Nordeste Carnes",
    "Império Store Maceió",
    "Emporio do Aço",
    "Empório da Pizza",
    "Anis Estrela - licores artesanais",
    "Baru Clothes",
    "Acarajé do baru",
    "Ponto do Suco",
    "Suco Bagaço",
    "Sucolândia",
    "Sabor Tropical - Açaí e Sucos Energéticos",
    "Nature sucos & sanduiches",
    "TropiKana",
    "Indústria de suco pronts LTDA",
    "Rice's Sucos e Lanches",
    "Mister Suco Saladeria",
    "Êbah Sucos",
    "NatuSuco/LanchesMcz",
    "Polpa de Fruta- Sucolândia Serraria",
    "Açaí Topadão"
]

# Executa a consulta das empresas
consulta_empresas(empresas)
