# Web Scraper - Memórias RAM
Este web scraper tem como objetivo extrair informações de preço e descrições de memórias RAM do site Kabum. Os dados são exportados para um arquivo .CSV, facilitando a análise posterior.

## Bibliotecas e dependências
- Python 3.8
- BeautifulSoup 4.9.1 (com *requests 2.24* para baixar as páginas do servidor)
- Pandas 1.1.1 (para formatar e exportar os dados extraídos)

## Atributos extraídos
Os atributos de cada produto foram deliberadamente selecionados:
- Título do anúncio
- Preço à vista
- Preço à prazo
- Avaliação (número de estrelas)
- Quantidade de avaliações recebidas

## Problemas e erros conhecidos
- Por algum motivo, as vezes ao executar o script, o Selenium não encontra a id da listagem de produtos e retorna uma exceção. Isso pode ser contornado executando o código novamente.

#TODO: Melhorar o tratamento de exceções
