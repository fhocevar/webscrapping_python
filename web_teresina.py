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
        url = f'https://www.google.com/search?q={nome_empresa_codificado}+teresina'  # Alterado para Teresina
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
    with open('empresas_teresina_TEL.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_teresina_TEL.csv com {len(dados_empresas)} registros.")

empresas = [
    "Tyago da Castanha",
    "Vanessa Castanhas",
    "Naturalíssima",
    "Partum Grãos",
    "Castanhas Store",
    "Ponto das Especiarias",
    "Castanhas Sabor do Piauí",
    "Nortista Confecções",
    "Cia da Saúde - Centro Norte, 308",
    "Cia da Saúde • Teresina Jóquei",
    "Sam’s Club",
    "Mahogany - Teresina Centro",
    "Mahogany - Teresina Shopping",
    "Mundo Verde",
    "Mahogany - Riverside Shopping",
    "Depósito de Banana Musa",
    "Empório da Banana",
    "Panda Banana Ateliê",
    "Caju Hortifruti",
    "Cajú Espetto's",
    "Caju Importados",
    "Caju Nordeste",
    "Brasucos - Fornecedor de Sucos de Caju / Cajuína",
    "Caju Mirim | Moda Infantil em Teresina",
    "Edifício Ilha do Caju",
    "Morena Caju",
    "Flor de Caju",
    "Caju Galerie",
    "Acajú",
    "Império Doce - Cajuça",
    "Caju",
    "Cantinho do Caju - Clube de Poker dos Amigos",
    "Restaurante Cajuí",
    "Cajuaça",
    "Maninho Atacadista - Matriz",
    "Rei do Atacado",
    "Atacadão - Teresina Primavera",
    "Atacadão - Teresina Ladeira do Uruguai",
    "Atacadão - Teresina Ilhotas",
    "Atacadão - Teresina Bela Vista",
    "Maninho Atacadista - Dom Severino",
    "Maria Bonita Distribuidora",
    "Atacadão de Fraldas e Variedades | Delivery em Teresina",
    "Atacadão Multimarcas The",
    "Assaí Atacadista",
    "Shopping Limas Atacado",
    "Assai Wholesaler Teresina",
    "Assaí Atacadista",
    "Atacadão dos Pés",
    "Gasper Atacado",
    "Ibyte Atacado Teresina",
    "JK Atacado Dirceu",
    "SOS Atacado",
    "Shop Atacado",
    "Mercado Central",
    "Extra Mercado",
    "Pão de Açúcar",
    "Ferreira Supermercados - Lourival Parente",
    "Assai Wholesaler Teresina",
    "Pão de Açúcar",
    "Assaí Atacadista",
    "Mercado Público do Parque Piauí",
    "Supermercado Aragão (Rede Super Dez)",
    "Mercado Do Dirceu I",
    "Carvalho Super Homero Castelo Branco",
    "Mercado São José",
    "Mercado Público Augusto Ferro (Mercado do Mafuá)",
    "Mercado Público Laurindo Veloso (Mercado da Vermelha)",
    "Pão de Açúcar",
    "Supermarket Sao Braz",
    "Supermarket Sao Braz",
    "Carvalho Super Riverside",
    "Ferreira Atacarejo",
    "Atacadão - Teresina Ilhotas",
    "The Emporium Bella",
    "Empório do Zeca",
    "The Emporium Bella",
    "Empório Sudeste Prime",
    "Empório Bella The",
    "Empório Flora Pura Teresina - Loja e Distribuidora Oficial",
    "Bella The - Café de Fátima",
    "Empório Fribal",
    "Empório",
    "Enayram Distribuidora",
    "Emporio Perfumes",
    "Mais Açaí Empório | A Melhor Açaiteria de Gurupi, Teresina",
    "Emporium Churrasqueiras",
    "Pecattu BWC Emporium Teresina - Distribuidora - Vinho - Bebidas",
    "Emporium Cães e Gatos",
    "Mercado dos Grãos - Produtos a Granel, Naturais, Carnes, Peixes e Suplementos",
    "Lili Doces",
    "Armazém Paraíba - Teresina Shopping",
    "HIT Store",
    "Armazém Dom Severino",
    "Enayram Distribuidora",
    "Kennedy Bebidas 24h",
    "Petrichor Licor",
    "Kennedy Bebidas Sul",
    "iBeer Bebidas",
    "Wcarnes Prime",
    "Papa-léguas Beer | Depósito de Bebidas",
    "Vichy Café",
    "Carvalho Super Homero Castelo Branco",
    "O Pesqueirinho",
    "Emporio Diave",
    "Lima Licor",
    "Varanda Boteco",
    "B.arte"
]

# Executa a consulta das empresas
consulta_empresas(empresas)
