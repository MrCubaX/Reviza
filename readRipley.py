from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
import json
import pymysql
from datetime import datetime

ROOT_URL = 'https://simple.ripley.com.pe/tecnologia/audifonos'
TAXONOMY_FALABELLA_URL = 'https://simple.ripley.com.pe/tecnologia/audifonos'
#__NEXT_DATA__ = 'return document.getElementsByTagName("script")[18].innerHTML'
tipo = '\'application/ld+json\''
__NEXT_DATA__ = 'return document.querySelectorAll("script[type='+ tipo +']").item(0).innerHTML'

HOST_BBDD = 'localhost'
PORT_BBDD = 3306
USER_BBDD = 'root'
PASS_BBDD = 'mabeliux14'
NAME_BBDD = 'reviza'
_MARKET = 'ripley'

connToMysql = pymysql.connect(host=HOST_BBDD,
                              port=PORT_BBDD,
                              user=USER_BBDD,
                              passwd=PASS_BBDD,
                              db=NAME_BBDD)

optionsOfWeBrowser = webdriver.ChromeOptions()
optionsOfWeBrowser.add_experimental_option(
    "excludeSwitches", ["enable-logging"])
optionsOfWeBrowser.add_argument('--start-maximized')
webBrowser = webdriver.Chrome(
                        options=optionsOfWeBrowser,
                        executable_path='drivers/chromedriver/chromedriver.exe')


def getLinksOfMenu():
    NumberOfPages = 29

    for paginaActual in range(0,NumberOfPages):
        webBrowser.get(TAXONOMY_FALABELLA_URL +'?page=' + str(paginaActual + 1))
        print(TAXONOMY_FALABELLA_URL+'?page=' + str(paginaActual + 1))
        try:
            valor = webBrowser.execute_script(__NEXT_DATA__)
        except:
            valor = 'nada'
            print('Error no funciono el script')
        #datos = json.loads(valor)
        readJSON(valor)
        #print(__NEXT_DATA__)
        #print(valor)


def readJSON(taxonomyOfWeb):
    data = json.loads(taxonomyOfWeb)
    for categories in data['itemListElement']:
        cur.execute('INSERT INTO categorias (name, description) VALUES (%s, %s)',
                    ('audifonos-ripley', 'audifonos'))
        cur.connection.commit()
        idCategory = cur.lastrowid
        # print(categories['position'])
        # print(categories['item']['name'])
        # print(categories['item']['brand'])
        # print(categories['item']['offers']['price'])

        productId = categories['item']['sku']
        skuId = categories['item']['sku']
        merchantCategoryId = categories['item']['sku']
        displayName = categories['item']['name']
        productType = 'Audifono'
        url = categories['item']['url']
        brand = categories['item']['brand']
        regular_price = categories['item']['offers']['price']
        real_price = categories['item']['offers']['price']


        cur.execute('INSERT INTO productos(productId, skuId, merchantCategoryId, displayName, productType, url, brand, Precio_regular, Precio_Oferta, IdPadre,market) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', 
                                                   (productId, skuId, merchantCategoryId, displayName, productType, url, brand, regular_price, real_price, idCategory, _MARKET ))
        cur.connection.commit()



def browseIntoSite(urlSiteToVisit):
    webBrowser.get(urlSiteToVisit)
    numberOfPages = webBrowser.find_element_by_class_name(
        'jsx-1738323148 jsx-1104282991 pagination-button').value
    print(numberOfPages)
    pageSource = webdriver.page_source
    pageSourceParse = BeautifulSoup(pageSource, 'html.parser')
    for productosList in pageSourceParse.findAll(name='div', attrs={'class': 'jsx-3686231685 product-name fa--product-name'}):
        print('Título del producto: ' + productosList.get_text())


cur = connToMysql.cursor()
cur.execute('USE reviza')

print('\nEl Crawler inicia a las '+ str(datetime.now()) + '\n' )
getLinksOfMenu()
print('\nEl Crawler finalizó a las '+ str(datetime.now()))
cur.close()
connToMysql.close()
webBrowser.close()

# def getLinksOfWeb():
#     linksCount = 0
#     linksFound = []

#     for allHREF in pageSourceParse('a', attrs={'href': re.compile('^(/falabella-pe/category/cat.)')}):
#         linksCount = linksCount + 1
#         if allHREF.attrs['href'] not in linksFound:
#             linksFound.append(allHREF.attrs['href'])
#     print(len(linksFound))

# getLinksOfWeb()


def visitLinksOfWeb(linksJSON):
    print('')


def getJSONOfWeb(url):
    print('')


def getNumberOfPages(jsonString):
    print('')
