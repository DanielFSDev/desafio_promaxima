# Desafio

# Tecnologias

- Python 3.7.5
- SQLite
- Docker
- Pandas 
- BeatifulSoup
- openpyxl
- pyxlsb

# Como rodar o projeto?

1. Entrar na pasta desafio: `cd desafio`
2. Executar o comando: `docker compose up -d --build --force-recreate`

# Como utilizar a aplicação?

1. Acessar `http://localhost:8000/scraping/inicial/`
2. Baixar as planilhas `Baixar arquivos` Observação: Baixar as planilhas irá demorar alguns minutos. (Ao terminar de baixar uma planilha, é salvo um registro na tabela 'planilha')
3. Após finalizar de baixar as planilhas
4. Clicar em `Planilhas baixadas`
5. Selecionar a planilha desejada e clicar em `Acessar dados` (Ao acessar dados, é salvo registros na tabela 'dados' de todos os dados processado da planilha. Antes de salvar esses registro, verifico se não existir já para evitar duplicidade).

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
