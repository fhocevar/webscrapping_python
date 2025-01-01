import requests
from bs4 import BeautifulSoup

# Função para extrair dados de uma página
def extrair_dados(url):
    # Requisição para obter o conteúdo da página
    response = requests.get(url)
    
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Criação do objeto BeautifulSoup para parsing
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extração do nome da empresa, telefone e e-mail
        # Dependendo da estrutura da página, altere as tags e classes conforme necessário
        nome_empresa = soup.find('h1').text  # Exemplo de captura de título (pode variar)
        telefones = soup.find_all('a', href=True)  # Captura de links (geralmente telefones estão em <a href="tel:...")
        emails = soup.find_all('a', href=True)  # Captura de links (geralmente emails estão em <a href="mailto:...")
        
        # Filtrando os dados encontrados
        lista_telefones = [tel.get('href') for tel in telefones if 'tel:' in tel.get('href')]
        lista_emails = [email.get('href') for email in emails if 'mailto:' in email.get('href')]
        
        # Exibindo os dados extraídos
        print(f"Nome da Empresa: {nome_empresa}")
        print("Telefones encontrados:", lista_telefones)
        print("E-mails encontrados:", lista_emails)

    else:
        print(f"Erro ao acessar o site: {response.status_code}")

# URLs dos sites para scraping
urls = [
    "https://florenzanonuts.com/br/contatos/",
    "https://castanhadoparanutriaco.com.br/representantes-de-castanha-do-para/",
    "https://imaflora.org/contato/mensagem",
    "https://www.cooperativacomaru.com/"
]

# Iterando sobre cada URL para extrair os dados
for url in urls:
    print(f"\nExtraindo dados de: {url}")
    extrair_dados(url)
