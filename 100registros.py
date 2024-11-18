from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
import csv

# Configuração do Selenium com o WebDriverManager
chrome_options = Options()
chrome_options.add_argument("--headless")  # Se desejar rodar sem interface gráfica
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Usa o WebDriverManager para obter o ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Aqui você pode usar o Selenium para navegar e coletar dados adicionais, se necessário.
driver.get("https://www.google.com")
print(driver.title)  # Exemplo de uso do Selenium: printa o título da página inicial do Google

driver.quit()  # Fecha o navegador após o uso

def consulta_empresas(empresa_list):
    api_key = 'SUA_CHAVE_API'  # Substitua pela sua chave API válida
    dados_empresas = []  # Lista para armazenar os dados de todas as empresas
    
    for nome_empresa in empresa_list:
        url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={nome_empresa}&key={api_key}'
        response = requests.get(url)
        data = response.json()

        if 'results' in data:
            for result in data['results']:
                nome = result.get('name', 'Nome não disponível')
                endereco = result.get('formatted_address', 'Endereço não disponível')
                telefone = result.get('formatted_phone_number', 'Telefone não disponível')
                website = result.get('website', 'Website não disponível')
                celular = telefone if telefone.startswith('+55 9') else 'Telefone não disponível como celular'  # Exemplo para diferenciar celular (Brasil)

                # CNPJ não disponível via Google Places API
                cnpj = 'CNPJ não disponível'

                # Armazena as informações em uma lista
                dados_empresas.append([nome, endereco, telefone, celular, website, cnpj])

                # Limite de 100 registros
                if len(dados_empresas) >= 100:
                    break

        # Se já atingiu 100 registros, sai do loop
        if len(dados_empresas) >= 100:
            break

    # Salvando os dados em um arquivo CSV
    with open('empresas.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Telefone', 'Celular', 'Website', 'CNPJ'])  # Cabeçalho
        writer.writerows(dados_empresas)  # Escreve os dados das empresas

    print(f"Dados salvos em empresas.csv com {len(dados_empresas)} registros.")

# Exemplo de lista de empresas
empresas = ["castanhas", "nozes", "macadamia", "banana passa", "pecan", "caju"]
consulta_empresas(empresas)
