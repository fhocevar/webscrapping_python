from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager

# Função para inicializar o Selenium
def get_driver():
    driver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=driver_service)
    return driver

# Função para buscar no Google e obter os links
def search_google(query, driver):
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)  # Esperar os resultados carregarem
    
    links = []
    search_results = driver.find_elements(By.CSS_SELECTOR, 'div.yuRUbf > a')
    for result in search_results:
        links.append(result.get_attribute("href"))
    
    return links

# Função para listar sites das empresas
def list_sites_for_companies():
    driver = get_driver()
    empresas = [
        "Florenzano Nuts",
        "Castanha do Pará Nutriaco",
        "Imaflora",
        "Fábrica de Castanha Benedito Mutran e Cia Ltda",
        "Cooperativa Comaru",
        "Castanheiras do Pará Ltda.",
        "Castanheiras do Brasil",
        "Associação de Produtores de Castanha do Brasil (APCB)",
        "Cooperativa dos Castanheiros de Cacoal (COOCACOAL)",
        "Fazenda Castanheira",
        "Associação dos Produtores de Castanha do Amapá (APCA)",
        "Cooperativa Agroextrativista do Xingu (CAX)",
        "Cooperativa dos Produtores de Castanha do Maranhão (COOPCAST)",
        "Sementes do Brasil (Sembra)",
        "Fazendas Extrativistas do Norte",
        "Indústria Castanheira Brasil",
        "Fazenda São Luiz",
        "Castanha do Amazonas Ltda.",
        "Cooperativa dos Produtores de Castanha do Xingu (COOPCAX)",
        "Castanheira do Brasil Indústria e Comércio",
        "Cooperativa dos Castanheiros do Pará (COOPCASTANHEIRO)",
        "Agroindústria Castanheiras do Brasil",
        "Santos Castanha",
        "Indústria de Castanha-do-Pará São Francisco",
        "Amazônia Castanha",
        "Cooperativa Agropecuária de Castanheiras de Rondônia",
        "Castanha do Norte Ltda.",
        "Castanha e Cia",
        "Tipico Ceará"
    ]
    
    all_links = {}
    for empresa in empresas:
        print(f"Buscando sites para: {empresa}")
        links = search_google(empresa, driver)
        all_links[empresa] = links
        print(f"Links encontrados para {empresa}: {links}")
    
    driver.quit()  # Fechar o driver após terminar a busca
    return all_links

if __name__ == "__main__":
    sites = list_sites_for_companies()
    print("\nLinks encontrados para as empresas:")
    for empresa, links in sites.items():
        print(f"\n{empresa}:")
        for link in links:
            print(link)
