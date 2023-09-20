import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# Constantes
SITE_URL = 'https://www.kabum.com.br/'
TERMO_PESQUISA = 'Processador'
NUM_PAGS = 5
NOME_ARQUIVO = "{}_{}.csv".format(TERMO_PESQUISA, datetime.datetime.now().strftime("%d%m%Y%H%M"))

def extrair_infos_produto(produto):
    titulo = produto.find('span', class_='nameCard').text
    preco_a_vista = float(produto.find('span', class_='priceCard').text.split('R$')[1].replace('.', '').replace(',', '.'))
    avaliacao = len(produto.find_all('div', class_='estrelaAvaliacao'))
    qtde_avaliacao = int(produto.find('div', class_='labelTotalAvaliacoes').text[1:-1]) if produto.find('div', class_='labelTotalAvaliacoes') else 0
    return titulo, preco_a_vista, avaliacao, qtde_avaliacao

# Inicializando o webdriver
driver = webdriver.Firefox()
driver.get(SITE_URL)

# Buscar
campo_busca = driver.find_element(By.ID, value='input-busca')
campo_busca.send_keys(TERMO_PESQUISA)
campo_busca.send_keys(Keys.ENTER)

# Listas para armazenar os dados
titulos = []
precos_a_vista = []
avaliacoes = []
qtde_avaliacoes = []

# Inicia o loop de cada página
p = 1
while p <= NUM_PAGS:
    try:
        time.sleep(2)
        print(f"Lendo página {p}...")

        # Inicia a extração das informações
        try:
            html = driver.find_elements(By.TAG_NAME, 'main')[0]
        except IndexError as ie:
            driver.refresh()
            continue

        html = html.get_attribute("innerHTML")

        sopa = BeautifulSoup(html, 'lxml')
        
        for item in sopa.find_all('div', {'class': 'productCard'}):
            titulo, preco_a_vista, avaliacao, qtde_avaliacao = extrair_infos_produto(item)
        
            titulos.append(titulo)
            precos_a_vista.append(preco_a_vista)
            avaliacoes.append(avaliacao)
            qtde_avaliacoes.append(qtde_avaliacao)
            
        driver.find_element(By.CLASS_NAME, 'nextLink').click()
        
        p += 1

        if p > NUM_PAGS:
            print("Extração concluída.")
            break
    except Exception as e:
        print("Exceção:", e)
        break

# Fechando o webdriver
driver.close()

# Criando o DataFrame com as listas
df = pd.DataFrame()
df["Nome"] = titulos
df["Preco_a_vista"] = precos_a_vista
df["Avaliacao"] = avaliacoes
df["Qtde_Avaliacoes"] = qtde_avaliacoes

print(f"\n{len(df)} registros adicionados.")

# Exportando para CSV
df.to_csv(NOME_ARQUIVO, index=False)
print(f"Arquivo salvo como {NOME_ARQUIVO}.")