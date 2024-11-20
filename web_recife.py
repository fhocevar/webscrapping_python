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
        url = f'https://www.google.com/search?q={nome_empresa_codificado}+recife'  # Alterado para São Luís
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
    with open('empresas_recife_TEL.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_recife_TEL.csv com {len(dados_empresas)} registros.")

# Lista de empresas em São Luís
empresas = [
    "Amendolândia",
    "FB Distribuidora - Produtos Naturais",
    "Casa Pedro Ferreira - Produtos Saudáveis",
    "Grão Empório Natural",
    "Saulo Temperos - Ceasa",
    "Grão em Grão Empório",
    "Empório Pura Vida",
    "Luciano D' Sertão",
    "Emporium Sweet Life",
    "Real Vida Produtos Naturais",
    "Costa Nova Alimentos",
    "Mendez Empório Nordestino",
    "Empório Ferreira Produtos Naturais",
    "Castanhora Empório Natural",
    "Emporio 23",
    "Mercearia Só Temperos",
    "Chá Verde - Grãos e Produtos Naturais",
    "Paço 23 | Mercado e Produtos Naturais Recife",
    "Mercado de São José - Recife",
    "Noz Confeitaria Por Ana Sophia",
    "Macadâmia - Confeitaria Saudável",
    "Cajueiro",
    "Caju Digital Agency",
    "Terminal Cajueiro",
    "Casa Cajueiro",
    "ACA- Associação dos Moradores do Bairro de Cajueiro",
    "Cajutec",
    "Cajueiro square",
    "Pet Shop Cajueiro",
    "POSTO BRAZ CAJUEIRO",
    "Cajueiro Seco",
    "Atacado dos Presentes",
    "Atacadão - Recife Boa Viagem",
    "Atacadão",
    "Atacado Santana",
    "ATACADÃO IMPORTADOS",
    "Distribuidora Mix - Atacadista de Utilidades Domésticas",
    "Palácio Atacado",
    "Assaí Atacadista",
    "Novo Atacarejo Matriz",
    "Deskontão Atacado",
    "Repon Atacado e Varejo",
    "Recife Atacado - Lingerie",
    "Atacarejo Shop",
    "Varejão Distribuidora - Bebidas em Atacado e Varejo",
    "Mercado de São José - Recife",
    "Mercado da Boa Vista",
    "Extra Mercado",
    "Mercado da Encruzilhada",
    "Mercado da Madalena",
    "Mercado de Boa Viagem",
    "Mercado Público De Casa Amarela",
    "Mercado da Torre",
    "Mercado Público de Nova Descoberta",
    "RM Express - Santo Amaro",
    "Cold Water Market",
    "Carrefour Hipermercado",
    "Cordeiro public market",
    "Supermarket More You",
    "Pão de Açúcar",
    "Super Bompreço",
    "Mercado Público de Santo Amaro",
    "Empório Pura Vida",
    "Empório Ferreira Produtos Naturais",
    "Emporium Sweet Life",
    "Empório Cozeart",
    "Empório Carnes e Bebidas",
    "Empório Caxangá",
    "Empório Universitário",
    "Empório das Russas",
    "Emporium elements 4",
    "Empório Pernambucano",
    "Empório Arte Brasileira",
    "Empório Casa",
    "Empório HD",
    "Empório Doces e Salgados",
    "Empório Express",
    "ARMAZÉM DA CACHAÇA / CONVENIÊNCIA",
    "Bebidas de Pernambuco",
    "Casa Bebidas",
    "Ingá Vinhos Finos",
    "Natureza Produtos Mariano",
    "Entre Vinhos - Wine Bar",
    "Chef Galvão Empório",
    "Licor & Kana - Cachaçaria artesanal",
    "Pau do Indio",
    "seu boteco",
    "Duty Free",
    "Sabores de Nazaré - Licores & Cachaça",
    "Cafeteria Santa Clara Madalena",
    "Manos Restaurante e Bar",
    "Deskontão Atacado",
    "Santo Gole - Licoteria e Cachaçaria Artesanal",
    "Bora? Boteco",
    "Barú Marisquería",
    "Barteco",
    "Gelattos sucos e lanches",
    "Suco natural jaqueira",
    "Casa do Suco B-12",
    "DUKE SUCOS NATURAIS",
    "Casa do suco Recife",
    "Sucos Energéticos",
    "CABANNA SUCOS",
    "SABOR DO PARQUE - SUCOS E SANDUÍCHES NATURAIS"
]


# Executa a consulta das empresas
consulta_empresas(empresas)