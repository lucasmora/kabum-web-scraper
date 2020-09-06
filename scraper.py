import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd

# Configurando o webdriver e inserindo o termo de busca (Memória RAM 8gb)
nav = webdriver.Chrome('/usr/bin/chromedriver')
nav.get('https://www.kabum.com.br/')

campo_busca = nav.find_element_by_class_name('sprocura')
campo_busca.send_keys('Memória RAM 8gb')
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

# Número de páginas a serem lidas
n_pgs = 5

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
df["Preco_prazo"] = precos_prazo
df["Estrelas"] = estrelas
df["Avaliacoes"] = avaliacoes

print(f"\n{len(df)} registros adicionados.")

# Exportando para CSV
arq = "memoria_ram_8gb.csv"
df.to_csv(arq)
print(f"Arquivo salvo como {arq}")

# Fechando o webdriver
nav.close()