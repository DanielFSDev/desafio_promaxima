# Desafio

# Configurar ambiente virtual

1. Criar ambiente virtual: `python3 -m venv venv`
2. Utilizar comando para ativar ambiente virtual (Linux): `source venv/bin/activate`

# Como rodar o projeto?

1. Instalar dependências do projeto: `pip install -r requirements.txt`
2. executar script para criar banco de dados: `init_db.py`
3. rodar o projeto: `python manage.py runserver`

# Como utilizar a aplicação?

1. Acessar `http://localhost:8000/scraping/inicial/`
2. Baixar as planilhas `Baixar arquivos` Observação: Baixar as planilhas irá demorar alguns minutos.
3. Após finalizar de baixar as planilhas
4. Clicar em `Planilhas baixadas`
5. Selecionar a planilha desejada e clicar em `Acessar dados`

# Informações

O código utiliza:

- Django para gerenciar o backend e as views.
- SQLite como banco de dados para armazenar informações extraídas.
- Pandas para manipulação e leitura das planilhas.
- BeautifulSoup para raspagem de links das páginas web.

( Banco de Dados )
 Tabelas :
`planilha`
- `id`: Identificador único.
- `nome_arquivo`: Nome do arquivo baixado.
- `data_download`: Data em que o arquivo foi salvo.

`dados`
- `id`: Identificador único.
- `codigo`: Código do item na planilha.
- `descricao`: Descrição do item.
- `unidade`: Unidade de medida.
- `valor`: Valor registrado.
- `planilha_id`: Relaciona o dado à planilha correspondente.

# Pontos importantes
- Checagem de duplicidade: Arquivos duplicados são evitados tanto no download quanto no banco de dados.

- Automação e organização: O sistema automatiza desde o download até o processamento e exibição, facilitando o uso por pessoas não técnicas.

- Facilidade de extensão: A lógica modular permite adicionar novas funcionalidades ou expandir o suporte a diferentes layouts de planilhas.
