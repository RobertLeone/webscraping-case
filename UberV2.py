# Bibliotecas
import json
import requests
import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

# Coloque as urls de cada cidade desejada.
localities = ['Digite sua url do uber aqui']

# Lista e contador
url_ends = []
ix = 4


for all in localities:

    ix += 1

    print(f'{ix} de {len(localities)}')

    navegador = webdriver.Chrome()

    init = all

    navegador.get(init)

    sleep(6)

    first = 0

    while navegador.current_url == init:

        sleep(10)
        pesquisar = navegador.find_elements(By.CSS_SELECTOR, 'button')[-1]
        pesquisar.click()

        first += 1

        sleep(4)

    navegador.get(init)

    sleep(6)

    for events in range(0,first - 1):

        sleep(10)
        pesquisar = navegador.find_elements(By.CSS_SELECTOR, 'button')[-1]

        pesquisar.click()

    sleep(4)

    site = BeautifulSoup(navegador.page_source, 'html.parser')

    filtro = site.findAll('div', attrs={'class': 'ag b9'})

    url_rest = []

    for links in filtro:

        url = links.find('a')
        urls = url['href']
        url_rest.append([urls])

    index = 0
    print(len(url_rest))

    for htmls in url_rest:

        index += 1

        if '/br/store/' in htmls[0]:

            r = requests.get('https://www.ubereats.com' + htmls[0])

            if '<Response [200]>' == str(r):

                print(r)

                soup = BeautifulSoup(r.content, 'html.parser')

                sleep(3)

                script = str(soup.find_all("script", {"type": 'application/ld+json'})[0]).split(">")[1].split("<")[0]

                # Carrega o arquivo json
                data = json.loads(script)

                try:
                    context = data['@context']
                    tipo = data['@type']
                    source = data['@id']
                    nome = data['name']
                    endereco = data['address']
                    score = data['aggregateRating']
                    geo = data['geo']
                    menu = data['hasMenu']
                    image = data['image']
                    hours = data['openingHoursSpecification']
                    action = data['potentialAction']
                    price = data['priceRange']
                    cuisine = data['servesCuisine']
                    telefone = data['telephone']

                except KeyError:

                    context = data['@context']
                    tipo = data['@type']
                    source = data['@id']
                    nome = data['name']
                    endereco = 'n/a'
                    score = data['aggregateRating']
                    geo = data['geo']
                    menu = data['hasMenu']
                    image = data['image']
                    hours = data['openingHoursSpecification']
                    action = data['potentialAction']
                    price = data['priceRange']
                    cuisine = data['servesCuisine']
                    telefone = data['telephone']

                    print(context, tipo, source, nome, endereco, score, geo, menu, image, hours, action, price, cuisine,telefone)

                # Adiciona as informações na lista
                url_ends.append([context, tipo, source, nome, endereco, score, geo, menu, image, hours, action, price, cuisine,telefone])

                # Printa o index
                print(index)

            else:

                # Caso haja falha no request irá mostrar a URL
                print(r, htmls[0])

                continue

        else:

            print(htmls[0])

            continue

        # Transformar em dataframe no pandas
    dados = pd.DataFrame(url_ends,columns=['context', 'tipo', 'source', 'nome', 'endereco', 'score', 'geo', 'menu', 'image','hours', 'action', 'price', 'cuisine', 'telefone'])

    print(dados)

    dados.to_csv(f'{ix}.csv', index=False)