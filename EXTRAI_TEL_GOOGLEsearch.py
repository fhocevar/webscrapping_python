import requests
from bs4 import BeautifulSoup
from googlesearch import search

def buscar_site(nome_empresa):
    # Busca no Google o site da empresa
    query = f"{nome_empresa} site oficial"
    resultados = search(query, num_results=5)  # Faz uma busca com 5 resultados
    
    # Pega o primeiro resultado da pesquisa
    if resultados:
        return resultados[0]  # Retorna o primeiro link da busca
    return None

def extrair_dados_do_site(url):
    # Faz uma requisição HTTP para acessar o conteúdo da página
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Exemplo: tentar pegar o nome da empresa (usando tag 'h1' como exemplo)
        nome_empresa = soup.find('h1').text if soup.find('h1') else 'Nome não encontrado'
        
        # Encontrar telefone (usando padrão de links 'tel:' para telefones)
        telefones = soup.find_all('a', href=True)
        lista_telefones = [tel.get('href') for tel in telefones if 'tel:' in tel.get('href')]
        
        # Encontrar e-mails (usando padrão de links 'mailto:' para e-mails)
        emails = soup.find_all('a', href=True)
        lista_emails = [email.get('href') for email in emails if 'mailto:' in email.get('href')]
        
        print(f"Nome da Empresa: {nome_empresa}")
        print(f"Telefones encontrados: {lista_telefones}")
        print(f"E-mails encontrados: {lista_emails}")
    else:
        print(f"Erro ao acessar o site: {response.status_code}")

# Lista de empresas para pesquisar
empresas = ["Florenzano Nuts", "Castanha do Pará Nutriaco", "Imaflora", "Cooperativa Comaru"]

# Para cada empresa na lista, buscar o site e extrair os dados
for empresa in empresas:
    print(f"\nBuscando dados para: {empresa}")
    site = buscar_site(empresa)
    if site:
        print(f"Site encontrado: {site}")
        extrair_dados_do_site(site)
    else:
        print("Não foi possível encontrar o site.")
