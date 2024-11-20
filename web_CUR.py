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
        url = f'https://www.google.com/search?q={nome_empresa_codificado}+São+Paulo'
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
    with open('empresas_curitiba.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_saopaulo.csv com {len(dados_empresas)} registros.")

empresas = [
    "Castanha Brasil Granel & Cia.", "Sabores do Campo Castanhas, Farinhas e Creatinas no Atuba em Curitiba", "Casa da Castanha - loja online", 
    "Raízes e Folhas, Castanhas, Encapsulados, Chás, Farinhas especiais, Cereais, Integrais, vegano, sem glúten, sem lactose", 
    "Nutty Bavarian - Shopping Palladium", "Castanhas BACKER", "Castanha de Caju", "Nutty Bavarian", "Broto da Terra", 
    "Poise Natural", "Cereais Mistura Fina", "Nutty Bavarian - Shopping Mueller", "Requinte Produtos Naturais", 
    "Emporio 56 Mercado Municipal", "SidSol Produtos Naturais - Boqueirão", "Empório Cereal Produtos Naturais", 
    "Grão Caneca Produtos Saudáveis", "Camomile Natural Emporium", "Empório Iguaçu", "NeM Produtos Naturais", 
    "NOZ - Closet Compartilhado", "Quero Nozes", "Quebra-nozes-Bolos & Delícias", "Macadamia Concept", 
    "MACADÂMIA MERCADO SAUDÁVEL", "Banana’s Sênior", "Banana maçã & Cia Hauer", "Bananas Portão", 
    "Frutaria Banana Maçã & cia", "Ana Banana Hortifruti", "Tropical Banana", "Joe Bananas", "Bananas Terra Nova", 
    "Soul Bread", "Capim Limão Produtos Naturais", "CAT Caju - Centro Administrativo e Técnico Alfredo Gottardi", 
    "Caju Confeitaria Sem Glúten", "Empório de Caju", "Cana Caju Beachwear", "Kaju Burguer", 
    "Estetic Car Caju", "Super Big Wholesaler", "Max Atacadista Curitiba - Linha Verde", "Atacadão - Curitiba Fazendinha", 
    "Assaí Atacadista", "Salla", "Atacadão - Curitiba Boqueirão", "Atacadão - Curitiba Bairro Alto", 
    "Atacadão - Curitiba Av. Das Torres", "Atacadão - Curitiba Guaira", "Max Atacadista Hauer", 
    "Max Atacadista Curitiba - Bairro Alto", "Distribuidora São Pedro - Atacado de Armarinhos, Papelaria e Embalagens de Presentes", 
    "Super Pro Atacado (Curitiba)", "Atacado Sibras", "Atacadão - Curitiba Boa Vista", "Assaí Atacadista - Cristo Rei", 
    "Selfa Atacado", "Atacadão - Curitiba Arthur Bernardes", "Atacadão da BR - Loja de Roupas em Curitiba", 
    "Mercado Municipal de Curitiba", "Curitiba Supermercados", "Mercado Vince", "Mercado Central", 
    "Supermercado Curitiba", "Mercado Vince - Mercado no Centro de Curitiba", "Mercado Fontana", 
    "Max Mercado", "Supermercado Matriz - Praça Generoso Marques", "Supermercado Nacional", "Top Mercado", 
    "Mercado Bella Villa Juvevê", "Armazém Curitiba Mini Mercado", "Mercado Nene", "Gepetto Mercado Centro", 
    "Buy Mania", "Supermercado Gasparin", "Mercado", "Festval Centro Cívico", "Empório Top Mix", 
    "Merci Empório Batel - Cestas de presente em Curitiba, Vinhos, Cervejas, tábua de frios, Clube de vinhos", 
    "Scopel Cave & Emporium family", "Empório Palu", "Empório do Campo", "São José Market - Shopping Crystal", 
    "Empório Abba Mix", "Empório São José", "Empório e Adega Família Scopel", "Empório do Alimento Comércio de Alimentos", 
    "Empório Natural Curitiba", "Empório D’Gust - Mercado Municipal de Curitiba", "Empório Rosmarino", 
    "Emporium Muf's Café", "Empório Kaveh Kanes", "Empório da Gula Express", "Grés Gastronomia e Empório", 
    "Empório Winiarski", "Emporium Nattuvida", "Adega Brasil Delicatessen", "Cellar Brazil Auto Service", 
    "Dinho Bebidas - Loja Atacarejo", "Brazil Gourmet Cellar", "Adega Gold Kim Bebidas Importadas", 
    "Distribuidora Liquor Store", "Vô Milano Cachaçaria", "Decanter Curitiba Centro", "Bebidas Tissot"
]

# Executa a consulta das empresas
consulta_empresas(empresas)
