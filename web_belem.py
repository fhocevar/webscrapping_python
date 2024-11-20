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
        url = f'https://www.google.com/search?q={nome_empresa_codificado}+Belém'  # Alterado para Belém
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
    with open('empresas_Belem_TEL.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas_Belem.csv com {len(dados_empresas)} registros.")

# Lista de empresas
empresas = [
    "Belém Nuts Castanhas",
    "Barraca | Paraíso da Castanha",
    "Mutran Exportadora",
    "Castanha da Nivea",
    "Nutty Bavarian",
    "Casa das Amêndoas",
    "Castanha Florense",
    "Armazém Nutri Belém",
    "Paratini Beneficiamento e Comercio de Frutas Ltda",
    "GRÃO da GENTE | VAREJO de SUPLEMENTOS A GRANEL (Ervas, grãos, cosméticos, essências, aromaterapia)",
    "Reis das castanhas",
    "Iraê Castanhas E Doces",
    "Hiho Doces - Bombons Regionais",
    "Mercado Ver-o-Peso",
    "Moinho Central",
    "BMNuts",
    "Empório Saudável",
    "Conveniência Ver-o-peso Varejo & Atacado",
    "Divina Terra Belém",
    "Brasnut - Usina e Comércio de Castanhas",
    "NOZES MULTIMARCAS",
    "Loja Real Fashion",
    "MALA 10 STORE",
    "Top Marcas Cap",
    "Empório das Cestas",
    "Ice cream Santa Clara - Belem",
    "GMS Produtos Naturais",
    "Casa da Juventude Comunidade Católica - CAJU",
    "Comunidade Santo Antônio de Lisboa - CAJU",
    "Passagem Cajú",
    "ASSEMBLÉIA DE DEUS TEMPLO CAJU",
    "Coxinhas e Pastéis do Caju",
    "Açaí do caju",
    "Atacadão - Belém",
    "Atacadão - Belém Portal",
    "Assaí Atacadista",
    "Florida Varejo e Atacado",
    "Assaí Atacadista",
    "Tok Leve Atacado E Varejo",
    "Loja Atacadista",
    "Atacadão da 15",
    "ll multimarcas - atacadista Belém/PA",
    "Bella Ricca Atacado EIRELI",
    "+B Supermercados (Tapanã)",
    "Carol atacado",
    "Loja Linda, MANA!",
    "Belém Confecções Só Atacado",
    "Atacadão Globo Esporte",
    "Aryelle store atacado e varejo",
    "Atacadão Hiper Paraense",
    "Rota Atacado & Varejo",
    "MODA INTIMA varejo e Atacado",
    "Jessi Make Distribuidora",
    "Mercado Ver-o-Peso",
    "Lider Batista Campos",
    "+B Supermercados (Plaza)",
    "Econômico Meio a Meio - Umarizal",
    "Supermercado Cidade Marambaia",
    "Líder Doca",
    "+B Supermercados (Alcindo)",
    "Supermercado Du Bairro",
    "Supermercado São Paulo",
    "Preço Baixo Meio a Meio - Senador Lemos",
    "Supermercado Du Bairro",
    "Econômico Meio a Meio - Jurunas",
    "Supermercado 8 de Mais",
    "Francisco Bolonha Market (Meat Market)",
    "Meio meio Compre Bem Pedreira",
    "Supermercados Cidade Ltda.",
    "Líder Humaitá",
    "Líder Praça Brasil",
    "Líder Cidade Velha",
    "Assaí Atacadista",
    "Mercado Metrô Belém",
    "Emporium Belém",
    "Loja Meu Garoto - Cachaça com Jambu",
    "Grand Cru",
    "Cachaça with Jambu Genuine",
    "Cachaça com Jambu",
    "Cosanostra Café",
    "Bosque Sport Bar & Bowling (1° andar)",
    "Bistrô & Boteco",
    "Engenho Dedé",
    "Grill Mix Belém",
    "Baron Club - Bar e Restaurante",
    "Rebuw club",
    "Bêra Gastronomia",
    "Batistão Sucos - Wandenkolk",
    "Batistão Sucos",
    "Batistão Sucos Batista Campos",
    "Batistão",
    "Casa de Sucos",
    "Sucos Naturais Belem | Hit Mania Sucos Naturais da Fruta",
    "COMBU JUICE, SUCOS NATURAIS",
    "Guaraná Amazônia",
    "Lt sucos",
    "JH Sucos Naturais",
    "T-Sucos",
    "Manancial Sucos (A M da Fonseca)",
    "Rei do suco",
    "SUCOS DA HORA",
    "Josy Sucos",
    "Casa Ródney's Mix sucos e vitaminas",
    "Marcio's Lanches e Sucos",
    "SUCO NATURAL DA GESSICA",
    "Casa de sucos Deus proverá",
    "Bom do Pará",
    "Feira Orgânica Belém - Pará Orgânico - Produtos Apícolas",
    "Orgânia | Produtos Orgânicos em Belém do Pará",
    "Divina Terra Belém",
    "Gaia Produtos Naturais",
    "Mercado Puro Natural",
    "Nação Verde - Belém do Pará"
]


# Executa a consulta das empresas
consulta_empresas(empresas)
