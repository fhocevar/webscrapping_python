# webscrapping_python
---

# Consulta Empresas via Google Places API

Este projeto consulta informações de empresas através da API do Google Places e salva os dados obtidos em um arquivo CSV. Ele faz buscas baseadas em uma lista de nomes de empresas, restringindo a busca à cidade de São Paulo - SP.

## Descrição

Este script utiliza a API **Google Places** para buscar informações sobre empresas, como **nome**, **endereço**, **telefone**, e um campo para **CNPJ** (que não é fornecido pela API diretamente). Ele salva os dados obtidos em um arquivo CSV chamado `empresas_sao_paulo.csv`.

## Funcionalidade

1. **Consulta via Google Places API**: O script consulta informações sobre empresas em São Paulo, utilizando os nomes fornecidos em uma lista.
2. **Limitação de 1000 Registros**: O script faz uma pausa assim que 1000 registros são coletados.
3. **Salvamento em CSV**: Os dados coletados (nome, endereço, telefone e CNPJ) são salvos em um arquivo CSV.

## Requisitos

- **Python 3.x** (Recomenda-se a versão 3.6 ou superior).
- **Bibliotecas Python**: 
  - `requests`: Para fazer requisições HTTP à API Google Places.
  - `csv`: Para manipulação de arquivos CSV.

### Instalar dependências

Se você não tem as dependências necessárias, pode instalá-las com o seguinte comando:

```bash
pip install requests
```

## Como Usar

### 1. Obtenção da Chave API do Google

- Você precisa de uma **chave API válida do Google Places** para usar este script.
- Para obter sua chave, siga as instruções no [Google Places API](https://developers.google.com/maps/documentation/places/web-service/overview).

Substitua a chave API no código:

```python
api_key = 'Sua_chave_API_aqui'  # Substitua pela sua chave API válida
```

### 2. Configuração da Lista de Empresas

Você pode personalizar a lista de empresas que deseja consultar, modificando o conteúdo da variável `empresas`. Exemplo:

```python
empresas = ["castanhas", "nozes", "macadamia", "banana passa", "pecan"]
```

### 3. Executando o Script

Após substituir a chave API e personalizar a lista de empresas, basta rodar o script no terminal:

```bash
python consulta_empresas.py
```

Isso irá iniciar o processo de consulta e salvar as informações em um arquivo `empresas_sao_paulo.csv`.

### 4. Saída

O script salvará um arquivo chamado `empresas_sao_paulo.csv` no diretório onde o script foi executado. Este arquivo terá as seguintes colunas:

- **Nome**: Nome da empresa.
- **Endereço**: Endereço da empresa (se disponível).
- **Telefone**: Número de telefone da empresa (se disponível).
- **CNPJ**: Este campo não é fornecido pela Google Places API, mas está incluído como um campo para uso futuro ou customização.

### Exemplo de estrutura do arquivo CSV:

```csv
Nome,Endereço,Telefone,CNPJ
Castanhas de São Paulo,Av. Paulista, 1000, (11) 98765-4321,CNPJ não disponível
Nozes e Produtos Naturais,Rua dos Três Irmãos, 2000, (11) 98765-1234,CNPJ não disponível
...
```

### 5. Limitações

- O script consulta até **1000 registros**. Se a lista de empresas for muito grande, ele interromperá a execução após atingir esse limite.
- Não é possível obter o **CNPJ** diretamente da API Google Places, então este campo será preenchido com "CNPJ não disponível".

## Contribuindo

Se você deseja contribuir para este projeto, siga estas etapas:

1. Faça o **fork** deste repositório.
2. Crie uma nova **branch** para a sua modificação.
3. Faça as alterações necessárias e **commit** suas mudanças.
4. Envie um **pull request** para revisar suas alterações.

## Licença

Este projeto está licenciado sob a **MIT License**. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Esse README fornece uma visão geral clara de como o script funciona e como configurá-lo e executá-lo corretamente.
