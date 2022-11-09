import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import datetime

site = 'https://www.kabum.com.br/'
termo_pesquisa = 'Placa de vídeo 4gb'
n_pgs = 5  # Número de páginas a serem lidas
nome_arquivo = "{}_{}.csv".format(termo_pesquisa, datetime.datetime.now().strftime("%d%m%Y%H%M"))  # Nome do arquivo a ser exportado

# Configurando o webdriver e inserindo o termo de busca (Memória RAM 8gb)
nav = webdriver.Firefox()
nav.get(site)

campo_busca = nav.find_element(By.ID, value='input-busca')
campo_busca.send_keys(termo_pesquisa)
campo_busca.send_keys(Keys.ENTER)
time.sleep(1)

# Cada atributo será armazenado numa lista correspondente
titulos = []
precos_a_vista = []
avaliacoes = []
qtde_avaliacoes = []

# Inicia o loop de cada página
p = 1
while True:
    try:
        time.sleep(2)
        print(f"Lendo página {p}...")

        # Inicia a extração das informações
        try:
            html = nav.find_elements(By.TAG_NAME, 'main')[0]
        except IndexError as ie:
            nav.refresh()
            continue

        html = html.get_attribute("innerHTML")

        sopa = BeautifulSoup(html, 'lxml')
        
        for i in sopa.find_all('div', {'class': 'productCard'}):
            titulo = i.find('span', {'class': 'nameCard'}).text
            preco_a_vista = i.find('span', {'class': 'priceCard'}).text
            avaliacao = len(i.find_all('div', {'class': 'estrelaAvaliacao'}))
            qtde_avaliacao = i.find('div', {'class': 'labelTotalAvaliacoes'})
            qtde_avaliacao = qtde_avaliacao.text[1:-1] if qtde_avaliacao is not None else 0
        
            titulos.append(titulo)
            precos_a_vista.append(preco_a_vista)
            avaliacoes.append(avaliacao)
            qtde_avaliacoes.append(qtde_avaliacao)
            
        nav.find_element(By.CLASS_NAME, value='nextLink').click()
        
        p += 1

        if p >= n_pgs+1:
            print("Extração concluída.")
            break
    except Exception as e:
        print("Exceção:", e)
        nav.refresh()

# Fechando o webdriver
nav.close()

# Criando o DataFrame com as listas
df = pd.DataFrame()
df["Nome"] = titulos

# Formatando os separadores de decimais
df["Preco_a_vista"] = precos_a_vista
df["Preco_a_vista"] = df["Preco_a_vista"].apply(lambda x: x.split('R$')[1].replace('.', '').replace(',', '.'))
df["Preco_a_vista"] = df["Preco_a_vista"].astype(float, errors='ignore')

df["Avaliacao"] = avaliacoes
df["Qtde_Avaliacoes"] = qtde_avaliacoes

print(f"\n{len(df)} registros adicionados.")

# Exportando para CSV
df.to_csv(nome_arquivo, index=False)
print(f"Arquivo salvo como {nome_arquivo}")
