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
        url = f'https://www.google.com/search?q={nome_empresa_codificado}+joinville'  # Alterado para Campinas
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
    with open('empresas_joinville_TEL.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_joinville_TEL.csv com {len(dados_empresas)} registros.")

# Lista de empresas em Campinas
empresas = [
    "Norteminas - Castanhas Selecionadas",
    "Empório das Castanhas - Mercado de Aperitivos",
    "Caju",
    "Caju",
    "Cajuri",
    "Caju Sport Nutrition - Suplementos Esportivos, Whey Protein, Creatina e Pre Treino",
    "Caju Moda",
    "HortifrutiMais Atacado de Frutas e Verduras",
    "Mercado Brasília",
    "Mercado Brasília",
    "Mercado Medeiros",
    "MG Mercearia Glória",
    "Supermercado Joinville",
    "Mercado Municipal de Joinville",
    "Mercado Belo",
    "Mercado Engenho",
    "Supermercado Vitorino",
    "Mercado Brasil",
    "Mercado & Açougue Joinvillense",
    "Mercado Téo",
    "Mercado Monsenhor",
    "Mercado Ponto Bom",
    "Giassi",
    "Mercado Jonck",
    "Supermercado Iguaçu",
    "Frutaria Monte Moriá",
    "Campos Salles market",
    "Mercado Triumphe",
    "Emporio de Minas",
    "A Pioneira Emporio Mineiro",
    "Empório Relíquias de Minas",
    "Sr.Suko",
    "China's Food & Açaí",
    "Uai Sucos",
    "Laranjet - Indústria e Comércio de Sucos",
    "Sukeria",
    "Restaurante Prosa di Minas",
    "Rei dos Sucos",
    "Minas Citro",
    "Vallejo",
    "Coco Bambu ItaúPower Contagem: Restaurante, Frutos do Mar, Camarão, Carnes, MG",
    "Graal Shopping",
    "Graal Oliveira",
    "Graal Bela Vista",
    "Graal Antares",
    "Graal Juiz de Fora",
    "Graal Estiva",
    "Graal Monlevade",
    "Graal Marfim",
    "Mira Lanches",
    "ibis Styles Poços de Caldas",
    "Orgânicos Joinville - Só delivery",
    "Alimentos Orgânicos Mattiola",
    "Feira de Produtos Orgânicos",
    "Verde Capim - Orgânicos, veganos e cruelty free",
    "Pura Vida Organic Groceries",
    "Cheirinho da Natureza",
    "Empório Ervas do Campo",
    "Fazendinha Salu.d Orgânicos e Naturais",
    "Casa Colina - Café Bistro & Empório",
    "Feira de Orgânicos: 'Do Mueller para a Mesa'",
    "Mumepo Agroecologia",
    "Orgânicos da Mantiqueira",
    "Armazém Zap",
    "GP Bebidas",
    "Guarana MINEIRO",
    "Mercado Brasília",
    "Mercado Brasília",
    "MG Mercearia Glória",
    "Drinks Jota Efe Ind. E Com. Ltda.",
    "Panificadora e confeitaria Stefani",
    "Atacadão - Patos de Minas",
    "Mercado Medeiros",
    "Refrigerantes do Triângulo",
    "Refrigerante Abacatinho",
    "Refrigerantes do Triângulo (Guaraná Mineiro CD Divinópolis MG)"
]

# Executa a consulta das empresas
consulta_empresas(empresas)
