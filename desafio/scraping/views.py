from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import os
from urllib.parse import urljoin
import re
import pandas as pd
from django.conf import settings
import sqlite3
from datetime import datetime

url_regioes = [
    'http://www.infraestrutura.mg.gov.br/component/gmg/page/2240-consulta-a-planilha-preco-seinfra-regiao-central',
    'http://www.infraestrutura.mg.gov.br/component/gmg/page/2241-consulta-a-planilha-preco-seinfra-regiao-jequitinhonha-e-mucuri',
    'http://www.infraestrutura.mg.gov.br/component/gmg/page/2242-consulta-a-planilha-preco-seinfra-regiao-leste',
    'http://www.infraestrutura.mg.gov.br/component/gmg/page/2243-consulta-a-planilha-preco-seinfra-regiao-norte',
    'http://www.infraestrutura.mg.gov.br/component/gmg/page/2244-consulta-a-planilha-preco-seinfra-regiao-sul',
    'http://www.infraestrutura.mg.gov.br/component/gmg/page/2245-consulta-a-planilha-preco-seinfra-regiao-triangulo-e-alto-paranaiba'
]

db_path = 'dados.db'

def inicial(request):
    return render(request, 'inicial.html')
    
def criarPastaPlanilhasSeNaoExistir():
    pasta_destino = os.path.join("downloads")
    caminho = "downloads/"
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    return caminho

def linkValidoParaDownload(link):
    return link.endswith('.xlsx') or link.endswith('.xlsb')

def baixar_arquivos(request):
    pasta_destino = criarPastaPlanilhasSeNaoExistir()
    urls_planilhas = []
    messages = []
    contarPlanilhasBaixadas = 0
    for url_regiao in url_regioes:
        tags = coletarTags(url_regiao)
        for tag in tags:
            link = tag['href']
            if linkValidoParaDownload(link):
                url_completa = montarUrlCompleta(link)
                if not arquivoExiste(url_completa, pasta_destino):
                    try:
                        contarPlanilhasBaixadas = contarPlanilhasBaixadas + 1
                        baixar_arquivo(url_completa, pasta_destino)
                    except Exception as e:
                        messages.append(f"Erro ao tentar baixar a planilha: {url_completa}, erro: {e}")
    messages.append(f"Quantidade de planilhas baixadas: {contarPlanilhasBaixadas}")
    return render(
        request,
        'inicial.html',
        {
            'regioes': url_regioes,
            'messages': messages,
            'urls_planilhas': urls_planilhas,
        })
    
def baixar_arquivo(url, destino):
    resposta = requests.get(url, stream=True)
    if resposta.status_code == 200:
        nome_arquivo = os.path.basename(url)
        caminho_arquivo = os.path.join(destino, nome_arquivo)
        with open(caminho_arquivo, 'wb') as arquivo:
            for chunk in resposta.iter_content(chunk_size=1024):
                arquivo.write(chunk)
        inserir_planilha_bd(nome_arquivo)
    else:
        raise Exception(f"Erro ao fazer o download do arquivo: {url}.")
    
def arquivoExiste(url_completa, pasta_destino):
    nome_arquivo = os.path.basename(url_completa)
    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
    return os.path.exists(caminho_arquivo)

def coletarTags(url_regiao):
    resposta = requests.get(url_regiao)
    if resposta.status_code == 200:
        soup = BeautifulSoup(resposta.text, 'html.parser')
        container = soup.find_all('div', class_='span-16 content last')
        for div in container:
            return div.find_all('a', href=True)
        
def montarUrlCompleta(href):
    url_completa = urljoin('http://www.infraestrutura.mg.gov.br/', href)
    url_completa = url_completa.replace("\\", "/")
    return url_completa        

def planilhas_baixadas(request):
    pasta_destino = "downloads/"
    arquivos_dados = []
    if os.path.exists(pasta_destino):
        arquivos = [f for f in os.listdir(pasta_destino) if f.endswith('.xlsx') or f.endswith('.xlsb')]
        for arquivo in arquivos:
            ano_mes_arquivo = re.match(r'(?P<data>\d{6})', arquivo)
            if ano_mes_arquivo:
                data = ano_mes_arquivo.group('data')
                data_formatada = f"{data[4:6]}-{data[:4]}"
                arquivos_dados.append({'arquivo': arquivo, 'data': data_formatada})
        arquivos_dados.sort(key=lambda x: x['data'], reverse=True)
    return render(request, 'visualizar_planilhas_baixadas.html', {'arquivos_dados': arquivos_dados})

def rasparDadosModeloNovo(pasta_arquivo):
    df = pd.read_excel(pasta_arquivo, sheet_name="Relatório", header=None)
    colunas = ['CÓDIGO', 'B', 'DESCRIÇÃO', 'D', 'E', 'F', 'UNIDADE', 'VALOR']
    df.columns = colunas
    df = df.iloc[28:]
    df = df[['CÓDIGO', 'DESCRIÇÃO', 'UNIDADE', 'VALOR']]
    df = df.dropna(how='any')
    return df.values.tolist()

def coletar_dados_planilha(request, arquivo):
    pasta_destino = os.path.join(settings.MEDIA_ROOT, 'downloads')
    pasta_arquivo = os.path.join(pasta_destino, arquivo)
    if os.path.exists(pasta_arquivo):
        xls = pd.ExcelFile(pasta_arquivo)
        sheet_names = xls.sheet_names
        planilha_id = pegar_id_planilha_db(arquivo)
        if "Relatório" in sheet_names:
            dados = rasparDadosModeloNovo(pasta_arquivo)
            for dado in dados:
                codigo, descricao, unidade, valor = dado
                inserir_dados_bd(codigo, descricao, unidade, valor, planilha_id)
            return render(request, 'visualizar_dados_novo.html', {'dados': dados})
        else:
            dados = {}
            abas = ["RODOVIÁRIAS", "EDIFICAÇÕES", "PROJETOS"]
            for aba in abas:
                if aba in sheet_names:
                    rasparDadosModeloAntigo(pasta_arquivo, aba, dados)
            for aba, valores in dados.items():
                for dado in valores:
                    codigo, descricao, unidade, valor = dado
                    inserir_dados_bd(codigo, descricao, unidade, valor, planilha_id)
                    return render(request, 'visualizar_dados.html', {'dados': dados})
    else:
        return render(request, 'visualizar_dados.html', {'erro': "Arquivo não encontrado"})
    
def rasparDadosModeloAntigo(pasta_arquivo, aba, dados):
    df = pd.read_excel(pasta_arquivo, sheet_name=aba)
    df = df.iloc[51:].dropna(how="all")
    df = df.drop(df.columns[1], axis=1)
    df = df.dropna(subset=[df.columns[0], df.columns[1], df.columns[2], df.columns[3]], how='any')
    dados[aba] = df.values.tolist()
    
def inserir_planilha_bd(nome_arquivo):
    data_atual = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO planilha (nome_arquivo, data_download) 
    VALUES (?, ?)
    """, (nome_arquivo, data_atual))
    conn.commit()
    conn.close()
    
def inserir_dados_bd(codigo, descricao, unidade, valor, planilha_id):
    conn = sqlite3.connect(db_path, timeout=2)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 1 FROM dados WHERE codigo = ? AND planilha_id = ?
    """, (codigo, planilha_id))
    resultado = cursor.fetchone()
    if resultado is None:
        cursor.execute("""
        INSERT INTO dados (codigo, descricao, unidade, valor, planilha_id)
        VALUES (?, ?, ?, ?, ?)
        """, (codigo, descricao, unidade, valor, planilha_id))
        conn.commit()
    conn.close()
    
def pegar_id_planilha_db(arquivo):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM planilha WHERE nome_arquivo = ?", (arquivo,))
    planilha_id = cursor.fetchone()[0]
    conn.close()
    return planilha_id