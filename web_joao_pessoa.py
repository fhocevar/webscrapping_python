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
        url = f'https://www.google.com/search?q={nome_empresa_codificado}+joao+pessoa+PB'  # Alterado para São Gonçalo, RJ
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
    with open('empresas_joaopessoa_TEL.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_joaopessoa_TEL.csv com {len(dados_empresas)} registros.")

empresas = [
    "Jacastanhas - Loja de Castanhas",
    "Box Da Castanha",
    "Casa das Castanhas - Saúde & Vida I Produtos Naturais Tambaú",
    "Castanholândia Produtos Regionais - Loja 8",
    "Loja da Castanha",
    "Natfrut - Produtos Naturais",
    "J&C Castanhas",
    "Ponto Natural JP Unidade João Câncio",
    "Le Nature Produtos Naturais - Loja Espaço Cultural",
    "Castanha House",
    "Vivenda dos Naturais",
    "Saúde em Grãos",
    "Nobrezas do Sertão",
    "Casa das Castanhas I Produtos Naturais - Centro",
    "Laury Naturais - Manaíra",
    "Le Nature Produtos Naturais - Quiosque Shopping Tambiá",
    "Ponto Natural Unidade Esperança",
    "Pimenta Arretada - (Temperos e Especiarias)",
    "Amorim Empório Natural João Pessoa",
    "Mercado Público de Tambaú",
    "éNozes",
    "Zôo nozes De João Pessoa",
    "Boteco de Noz",
    "Madoska Sorveteria Artesanal - João Pessoa",
    "Gratitude Empório Natural",
    "Bodega Brasileira - Produtos Naturais",
    "Conveniência - Empório Tem de Quê",
    "Mahogany Manaíra Shopping",
    "Banana",
    "Empresa Paraibana de Turismo S/A PBTUR",
    "Caju Square",
    "Caju Class Flat",
    "Dom Caju Bar e Petiscaria",
    "Oficina Caju Diesel",
    "Praça do Caju",
    "CAJU PERSONALIZADOS",
    "Casa caju",
    "Posto Cajueiro Com. de Derivados de Petroleo",
    "Cuiá",
    "Bar do Cajueiro",
    "Shake Bessa Jampa Praça do Caju",
    "Odara Caju Corretora De Imóveis",
    "Canoa dos Camarões",
    "Shake Édson Ramalho - Espaço Vida Saudável Marcos Caju",
    "Pousada Cabo Branco",
    "Armazém das Coisas PB",
    "Brazil Atacado",
    "Atacadão - João Pessoa",
    "Atacadão dos Presentes e Utilidades",
    "Assaí Atacadista",
    "Mangabeira Atacado",
    "SuperFácil Atacado",
    "Atacadão - João Pessoa - Atacado",
    "Boa Compra - Bom Negócio Até No Nome",
    "Atacadão Econômico - Distribuidora de Matérias de Construção",
    "CDS Atacadista",
    "O Baratão Atacado",
    "VM Atacado Distribuidora",
    "American Atacado",
    "Atacadão dos Presentes",
    "Central de Alimentos Quirino (Atacadão Lima)",
    "All Good Chicken",
    "Make no Atacado",
    "Correia Atacado",
    "Super Atacado Bom Todo - Ruy Carneiro",
    "Central das Frutas",
    "Mercado Público de Tambaú",
    "Supermercado Manaíra",
    "Mercado Público de Mangabeira",
    "Public Tower Market",
    "Supermercado São João",
    "Supermercado Tambaú",
    "Supermercado Rede Menor Preço",
    "Extra Mercado",
    "Mercado Jampa 24 Horas",
    "Pão de Açúcar",
    "Mateus Supermercados",
    "Pão de Açúcar",
    "Assaí Atacadista",
    "Supermercado Litoral",
    "Supermercado O Destakão",
    "Mercado do Bairro dos Estados",
    "Rede Menor Preço",
    "Supermercado Santo André",
    "Cristal Presentes",
    "Cremosinn Jampa",
    "Crystal Bijoux",
    "Cristal Iluminação",
    "Plásticos Kadoshi",
    "O Especialista em Farol",
    "Center Mix",
    "Cristal Premium Acessórios",
    "Cristal Box",
    "Naturali & Cia",
    "Babú Bebidas",
    "Supermercado Manaíra",
    "Central das Frutas",
    "Mega Suco",
    "Box Da Castanha",
    "Escala Fava Bar e Restaurante",
    "Aquarius Supermercado",
    "Bruno Bebidas",
    "Manaçai - Delivery",
    "Aquarius Supermercado (segunda menção)",
    "S.O.S Bebidas",
    "Cannelle Restaurante, Conveniência e Padaria",
    "Supermercado Latorre",
    "WM ACAITERIA",
    "Supermercado União",
    "Chegou a Feira | Supermercado",
    "Takashi",
    "Barraca Da Lenita",
    "Panda Lanches Lanchonete"
]



# Executa a consulta das empresas
consulta_empresas(empresas)
