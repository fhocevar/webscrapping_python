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
        url = f'https://www.google.com/search?q={nome_empresa_codificado}+foz+do+iguacu'  # Alterado para Campinas
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
    with open('empresas_foz_TEL.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_foz_TEL.csv com {len(dados_empresas)} registros.")

# Lista de empresas em Londrina

empresas = [
    "Nutty Bavarian",
    "Boutique das Castanhas",
    "Palácio dos Temperos e Produtos Naturais",
    "Pomare Empório - Produtos Naturais em Foz do Iguaçu",
    "Grãos SA - Atacarejo produtos naturais e especiarias",
    "Margherita Temperos",
    "Mayer´s Especiarias",
    "Cereais Iguaçu Ltda.",
    "Jeová Jireh Delícias",
    "Lr produtos naturais",
    "Castanha House",
    "Sodiê Doces Foz do Iguaçu",
    "Pronapi - Produtos Naturais em Foz do Iguaçu",
    "Kapadokya",
    "MANIA DO NORTE AÇAITERIA",
    "Doceria Kau Magnabosco",
    "Vivaz Produtos Naturais",
    "Divina Terra Foz do Iguaçu",
    "Jauense Confeitaria - Foz do Iguaçu",
    "Brasil Verde Centro - Foz do Iguaçu",
    "Atacadão - Foz do Iguaçu",
    "Chips de Banana, batata salsa, batata doce e inhame",
    "Papittos Chipps de Banana",
    "Caju torteria - Tortas Salgadas",
    "Além do Cacau - Shopping Catuaí Palladium",
    "Costa do Cacau - Fabrica de Chocolate Fino (Bean To Bar)",
    "CACAU - Centro Acadêmico de Arquitetura e Urbanismo",
    "Cacau Store - Loja de roupas femininas",
    "Cacau Show - Chocolates",
    "Max Atacadista JK - Foz do Iguaçu",
    "Muffato Max Atacadista",
    "Superdia Atacado - Foz do Iguaçu",
    "Porã Atacado",
    "Assaí Atacadista",
    "Dilettare Atacado e Varejo",
    "Destro Macroatacado",
    "Portí Atacadista Foz",
    "Atacado Empório da Moda",
    "Atacado Rodrigues",
    "Megacenter Atacado",
    "Comercial Dalas",
    "Atacado Jeans isneylemos",
    "Lingerie em Foz do Iguaçu - Atacado Lingerie Vila A",
    "Mônaco Atacado",
    "HORTA. ATACADO VERDURAS",
    "Coafaso Ceasa",
    "DannyFoz Comércio Confecções Representações Comerciais",
    "Super Muffato Foz do Iguaçu - Portinari",
    "Super Muffato - Boicy",
    "Líder Supermercado",
    "Ítalo Supermercados - Foz do Iguaçu Centro",
    "Amigão Supermercados - Foz do Iguaçu",
    "Ney Supermercado",
    "Ítalo Supermercados - Foz do Iguaçu Jd. Petrópolis",
    "Villa Pomar hortifruti",
    "Ítalo Supermercados - Foz do Iguaçu República",
    "Supermercado Pinheiro",
    "Supermercado Econômico",
    "Ítalo Supermercados - Foz do Iguaçu - Porto Meira",
    "Mercado Marroni",
    "Dia D Supermercado",
    "Mercado Mais Você",
    "Supermercado Bella",
    "Mercado e Açougue MM",
    "Mini Mercado Pontal",
    "Empório com Arte",
    "Empório da Vila Foz",
    "Empório da Vila",
    "Empório JK",
    "Empório Salam",
    "Emporium da Massa",
    "Empório da Villa - Bar, Petiscaria e Restaurante",
    "Imperio do Armazém",
    "Empório D'Ervas - Produtos Naturais",
    "Empório Natumel Produtos Naturais",
    "Império Importados",
    "Dega Empório - Frios e produtos naturais",
    "Padaria Monte Líbano | Foz do Iguaçu"
]

# Executa a consulta das empresas
consulta_empresas(empresas)
