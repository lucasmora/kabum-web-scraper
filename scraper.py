import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd

nav = webdriver.Chrome('/usr/bin/chromedriver')
nav.get('https://www.kabum.com.br/')

campo_busca = nav.find_element_by_class_name('sprocura')
campo_busca.send_keys('Memória RAM 8gb')
campo_busca.send_keys(Keys.ENTER)

time.sleep(1)

html = nav.find_element_by_id('listagem-produtos')
html = html.get_attribute("innerHTML")

sopa = BeautifulSoup(html, 'lxml')

titulos = []
precos_boleto = []
precos_prazo = []
estrelas = []
avaliacoes = []

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
            
        nav.find_element_by_class_name('hEjrXm').click()
        p += 1
        if p > 6:
            print("Extração concluída.")
            break
    except Exception:
        print("Próxima página não encontrada. Continuando...")
        break

df = pd.DataFrame(columns=["Nome", "Preco_boleto", "Preco_prazo", "Estrelas", "Avaliacoes"])
df["Nome"] = titulos
df["Preco_boleto"] = precos_boleto
df["Preco_prazo"] = precos_prazo
df["Estrelas"] = estrelas
df["Avaliacoes"] = avaliacoes

print(f"\n{len(df)} registros adicionados.")

arq = "memoria_ram_8gb.csv"
df.to_csv(arq)
print(f"Arquivo salvo como {arq}")

nav.close()