# Web Scraper - Kabum!

Este web scraper tem como objetivo extrair informações de preço e descrições de produtos do site [Kabum!](https://www.kabum.com.br). Os dados são exportados para um arquivo .CSV, facilitando a análise posterior.

## Bibliotecas e dependências

- Python 3
- Selenium 4.1 e *geckodriver*
- BeautifulSoup 4.9.3 com *requests 2.2* e *html5lib*
- Pandas 1.4

## Atributos extraídos

Os atributos de cada produto foram deliberadamente selecionados:

- Título do anúncio
- Preço à vista
- Avaliação (número de estrelas)
- Quantidade de avaliações recebidas