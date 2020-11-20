import sys
import getopt
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import re

site = 'https://www.kabum.com.br/'
termo_pesquisa = 'Memoria RAM 8gb'
n_pgs = 1  # Número de páginas a serem lidas
nome_arquivo = "memoria_ram_8gb.csv"  # Nome do arquivo a ser exportado

# Configurando o webdriver e inserindo o termo de busca (Memória RAM 8gb)
nav = webdriver.Firefox()
nav.get(site)

campo_busca = nav.find_element_by_class_name('sprocura')
campo_busca.send_keys(termo_pesquisa)
campo_busca.send_keys(Keys.ENTER)

# Aguarda 1 segundo para completar o carregamento
time.sleep(1)

# Inicia a extração das informações
html = nav.find_element_by_id("listagem-produtos")
html = html.get_attribute("innerHTML")

sopa = BeautifulSoup(html, 'lxml')

# Cada atributo será armazenado numa lista correspondente
titulos = []
precos_boleto = []
precos_prazo = []
estrelas = []
avaliacoes = []

# Inicia o loop de cada página
p = 1
while True:
    try:
        time.sleep(1)

        print(f"Lendo página {p}...")
        
        for i in sopa.find_all('div', {'class': 'eITELq'}):
            titulo = i.find('a', {'class': 'item-nome'}).text
            preco_boleto = i.find('div', {'class': 'qatGF'}).text
            preco_prazo = i.find('div', {'class': 'ksiZrQ'}).text
            estrela = i.find('div', {'class': 'cQXAKv'}).attrs['class'][-1]
            avaliacao = i.find('div', {'class': 'BbVno'}).text
        
            titulos.append(titulo)
            precos_boleto.append(preco_boleto)
            precos_prazo.append(preco_prazo)
            estrelas.append(estrela)
            avaliacoes.append(avaliacao)
            
        if p == n_pgs:
            print("Extração concluída.")
            break
            
        nav.find_element_by_class_name('hEjrXm').click()
        
        p += 1
    except Exception:
        print("Próxima página não encontrada. Continuando...")
        break

# Criando o DataFrame com as listas
df = pd.DataFrame(columns=["Nome", "Preco_boleto", "Preco_prazo", "Estrelas", "Avaliacoes"])
df["Nome"] = titulos

df["Preco_boleto"] = precos_boleto
df["Preco_boleto"] = df["Preco_boleto"].apply(lambda x: x.split(' ')[1].replace(',', '.'))
df["Preco_boleto"] = df["Preco_boleto"].astype(float)

df["Preco_prazo"] = precos_prazo
df["Preco_prazo"] = df["Preco_prazo"].apply(lambda x: x.split(' ')[1].replace(',', '.'))
df["Preco_prazo"] = df["Preco_prazo"].astype(float)

df["Estrelas"] = estrelas
df["Estrelas"] = df["Estrelas"].str.replace('e', '')
df["Estrelas"] = df["Estrelas"].astype(int)

df["Avaliacoes"] = avaliacoes
df["Avaliacoes"] = df.Avaliacoes.str.extract(r"(\d+)")
df["Avaliacoes"] = df["Avaliacoes"].astype(int)

print(f"\n{len(df)} registros adicionados.")

# Exportando para CSV
df.to_csv(nome_arquivo, index=False)
print(f"Arquivo salvo como {nome_arquivo}")

# Fechando o webdriver
nav.close()
