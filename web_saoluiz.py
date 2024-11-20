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
        url = f'https://www.google.com/search?q={nome_empresa_codificado}+São+Luís'  # Alterado para São Luís
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
    with open('empresas_Sao_Luis_TEL.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_Sao_Luis.csv com {len(dados_empresas)} registros.")

# Lista de empresas em São Luís
empresas = [
    "Castanha São Luís Maranhão - Delicia´s", "Mercado da Praia Grande", "Comercial Castanha", 
    "NATURAL PRODUCTS Muniz", "Empório Pami", "Guaraná Naturale", "Empório Família Saudável, Temperos, Suplementos, Sem Glúten, Sem lactose, em Cidade Operária",
    "Produtos Naturais Muniz", "Terra Viva Alimentos Naturais", "Produtos Naturais - Empório, Saúde e Vida", 
    "Tulhas artesanato e cia", "Muniz", "Natural Vida Alimentos Funcionais", "Mercado das Tulhas", "Central Market", 
    "Temperos da Ilha", "Empório Fribal", "Casa Real Empório", "Bolo Divinno Bolo", "Casa do amendoim e castanha", 
    "NOZ Neurocentro", "Praia do Cajueiro", "Cajupe", "CajuPary", "Porto Cajueiro - Escritório JCA", 
    "Sítio e Balneário Recanto do Caju", "Caju", "Cais do Cajupary", "Cajuré", "Bloco caju Novo tempo 2", 
    "Cajupary Bar", "Petiscaldos", "Cafofinho da Tia Dica", "Campo do Cajupary", "Cajupary City", "Barbearia Caju", 
    "Atacadão - São Luiz", "Atacadão do 12 (Atacado e Varejo)", "Atacado Moda Masculina - Shopping Da Ilha", 
    "Atacadão De Caruarú", "Oliveira Atacado", "Rei das confecções (atacado e varejo)", "Assaí Atacadista", 
    "Atacadão Têxtil", "Goiânia Fashion", "Maranhão Atacadista", "WS.atacadista", "ibyte Atacado Av. Dos Franceses | São Luís MA", 
    "Assaí Atacadista", "TUDO MODA Renascença", "Assaí", "DISTRIBUIDORA MARANHÃO", "Ldj", "Fortaleza Modas", 
    "Moda Colmeia: Moda Feminina, Vestidos, Conjuntos, São Cristóvão, São Luis MA", "Juliana Modas Atacado", 
    "Central Market", "Supermercados São Luís", "Mateus Supermercados", "Municipal Market", "Mercado das Tulhas", 
    "Mercado do São Francisco", "Supermercado Universo", "Fish Market", "Supermercado JP - Bairro de Fátima", 
    "Hiper Mateus - Jardim Renascença", "Market Vinhais", "São Luís Shopping", "Mateus Supermercados", 
    "São Luís Express", "Mercado da Praia Grande", "Varejão Felix", "Fair Praia Grande", "Mateus Supermercados - Bacanga", 
    "Supermercados J B", "São Luís", "Casa Real Empório", "Emporio Doll - São Luís", "Emporio Fish", "São Luís Shopping", 
    "Empório LS", "Emporium Saint Louis", "Mercado das Tulhas", "O Dom da Carne", "Armazém São Luís", "Emporio Paiva", 
    "Ki Papéis", "Conveniência empório Scuba", "Armazém do Chef", "São Luís Express", "Emporio Fish Gourmet", 
    "Empório Das Carnes", "Massamor | Empório de Massas em São Luís", "Empório das Meias", "Empório Lopes", 
    "Armazém Paraíba Tecidos", "Dona Licor", "Mandaí", "Italia Wine Bar", "Adega SLZ", "Córdoba Wine", 
    "Azeite e Sal Praia", "Dona Licor Divineia", "Ls Distribuidora", "Blue Tree Towers", "Baruck", "Baruc eventos", 
    "Baruk Variedades", "Baruc - Bar e Restaurante", "Sukeria do Mineiro", "Desfrut", "Casa de sucos Mais Sabor", 
    "Casa de Sucos Mix- Cohama", "Desfrut", "Açaí Concept", "Casa de Sucos Mix - Vinhais", "Suco Gold", "Guaraná Naturale", 
    "Sukêro Juice bar", "Menos 15 Graus - Polpas de Frutas"
]

# Executa a consulta das empresas
consulta_empresas(empresas)