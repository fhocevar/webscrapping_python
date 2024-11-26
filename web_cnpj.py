import requests
import time
import csv

def consulta_cnpj(cnpj, token):
    """Consulta dados de uma empresa pelo CNPJ usando a API da Hub do Desenvolvedor."""
    url = f"http://ws.hubdodesenvolvedor.com.br/v2/cnpj/?cnpj={cnpj}&token={token}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['return'] == "OK":
            return data['result']
    return None

def consulta_lista_cnpjs(cnpjs, token, output_file="empresas.csv"):
    """Consulta uma lista de CNPJs e salva os resultados em um arquivo CSV."""
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Escreve o cabeçalho
        writer.writerow(['CNPJ', 'Nome', 'Fantasia', 'Atividade Principal', 'CEP', 'Endereço', 'Telefone'])

        for cnpj in cnpjs:
            data = consulta_cnpj(cnpj, token)
            if data:
                # Extrai informações específicas do retorno
                nome = data.get("nome", "N/A")
                fantasia = data.get("fantasia", "N/A")
                atividade_principal = data.get("atividade_principal", {}).get("text", "N/A")
                cep = data.get("cep", "N/A")
                endereco = f"{data.get('logradouro', 'N/A')}, {data.get('numero', 'N/A')}"
                telefone = data.get("telefone", "N/A")
                
                # Escreve os dados no arquivo CSV
                writer.writerow([cnpj, nome, fantasia, atividade_principal, cep, endereco, telefone])

            # Tempo de espera para respeitar o limite de taxa da API
            time.sleep(1)  # Ajuste conforme o limite permitido pela API

    print(f"Consulta completa. Dados salvos em {output_file}")

# Exemplo de uso
token = "165357420XMLUJpSadN298547808"
lista_cnpjs = ["13481309000192", "12345678000199", "11223344000188"]  # Substitua por sua lista de CNPJs
consulta_lista_cnpjs(lista_cnpjs, token)
