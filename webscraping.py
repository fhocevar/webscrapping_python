import requests
from bs4 import BeautifulSoup

# URL de um diretório com empresas
url = "https://exemplo.com/diretorio-empresas"

# Requisição para obter o conteúdo da página
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Encontrar informações específicas, como nome e telefone da empresa
for empresa in soup.find_all('div', class_='empresa-listagem'):
    nome = empresa.find('h2').text.strip()
    telefone = empresa.find('span', class_='telefone').text.strip()
    print(f"Nome: {nome}, Telefone: {telefone}")
