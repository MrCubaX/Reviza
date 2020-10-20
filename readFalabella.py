from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
import json
import pymysql
from datetime import datetime

ROOT_URL = 'https://www.falabella.com.pe/falabella-pe'
TAXONOMY_FALABELLA_URL = 'https://www.falabella.com/s/content/v1/taxonomy/pe'
__NEXT_DATA__ = 'return document.getElementById("__NEXT_DATA__").innerHTML'
_MARKET = 'falabella'

HOST_BBDD = 'localhost'
PORT_BBDD = 3306
USER_BBDD = 'root'
PASS_BBDD = 'mabeliux14'
NAME_BBDD = 'reviza'

connToMysql = pymysql.connect(host = HOST_BBDD,
                              port = PORT_BBDD,
                              user = USER_BBDD,
                              passwd = PASS_BBDD,
                              db = NAME_BBDD)

optionsOfWeBrowser = webdriver.ChromeOptions()
optionsOfWeBrowser.add_experimental_option("excludeSwitches",["enable-logging"])
optionsOfWeBrowser.add_argument('--start-maximized')
webBrowser = webdriver.Chrome(
                        options=optionsOfWeBrowser,
                        executable_path='drivers/chromedriver/chromedriver.exe')


def getLinksOfMenu():
    webBrowser.get(TAXONOMY_FALABELLA_URL)
    taxonomyOfWeb = webBrowser.find_element_by_tag_name('pre').text
    readJSON(taxonomyOfWeb)


def readJSON(taxonomyOfWeb):
    data = json.loads(taxonomyOfWeb)
    for categories in data['state']['rootCategories']:
        cur.execute('INSERT INTO categorias (name, description) VALUES (%s, %s)',
                    (categories['label'], categories['link']))
        cur.connection.commit()
        idCategory = cur.lastrowid
        for subcategorias in categories['subCategories']:
            cur.execute('INSERT INTO subcategorias (name, description,idPadre) VALUES (%s, %s,%s)',
                        (subcategorias['label'], subcategorias['link'], idCategory))
            cur.connection.commit()
            idSubcategory = cur.lastrowid
            cantidadpaginas = 1
            paginaActual = 1
            cantidadLeaf = len(subcategorias['leafCategories'])
            #print('Tiene ' + str(cantidadLeaf) + ' items' )
            contadorCategory = 1
            for leaf in subcategorias['leafCategories']:
                if contadorCategory ==  cantidadLeaf:
                    print('\nSe Obvia la leafCategories '+ leaf['link'] + ' Saliendo al break!\n' )
                    break
                print( ROOT_URL + leaf['link'] + '?page=1')
                webBrowser.get(ROOT_URL + leaf['link'] + '?page=1')
                #webBrowser.get('https://www.falabella.com.pe/falabella-pe/category/cat12820462/Aspiradoras-Robot')
                time.sleep(3)
                try:
                    valor = webBrowser.execute_script(__NEXT_DATA__)
                except:
                    valor = ''
                    print('\nSe salta el link '+ ROOT_URL + leaf['link'] + '?page=' + str(paginaActual) + ' por no tener el script NEXT_DATA\n')
                    break
                datos = json.loads(valor)
                try:
                    contador = datos['props']['pageProps']['pagination']['count']
                    porPagina = datos['props']['pageProps']['pagination']['perPage']
                    cantidadpaginas = round(int(contador) / int(porPagina))
                    cantidadpaginas2 = cantidadpaginas * porPagina
                    if cantidadpaginas2 < contador:
                        cantidadpaginas = cantidadpaginas + 1
                    print(str(contador)+' Productos, se muestra '+ str(porPagina) + ' por página, se considerará ' + str(cantidadpaginas)+ ' páginas')

                    productId = datos['props']['pageProps']['results'][0]['productId']
                    skuId = datos['props']['pageProps']['results'][0]['skuId']
                    merchantCategoryId = datos['props']['pageProps']['results'][0]['merchantCategoryId']
                    displayName = datos['props']['pageProps']['results'][0]['displayName']                
                    productType = datos['props']['pageProps']['results'][0]['productType']
                    url = datos['props']['pageProps']['results'][0]['url']
                    brand = datos['props']['pageProps']['results'][0]['brand']
                    regular_price = datos['props']['pageProps']['results'][0]['prices'][0]['price'][0]
                    real_price =    datos['props']['pageProps']['results'][0]['prices'][0]['price'][0]
                except:
                    print('\n*****No tiene pagination, se asume que es una página de producto*****')

                    productId = datos['props']['pageProps']['productData']['id']
                    skuId = datos['props']['pageProps']['productData']['id'] #revisar el corecto
                    merchantCategoryId = datos['props']['pageProps']['productData']['merchantCategoryId']
                    displayName = datos['props']['pageProps']['productData']['name']                
                    productType = datos['props']['pageProps']['productData']['productType']
                    url = datos['props']['pageProps']['openGraphData']['canonicalUrl']
                    brand = datos['props']['pageProps']['productData']['brandName']
                    regular_price = datos['props']['pageProps']['productData']['variants'][0]['prices'][0]['price'][0]
                    real_price =    datos['props']['pageProps']['productData']['variants'][0]['prices'][0]['price'][0]           
                                                                                                                           

                cur.execute('INSERT INTO productos(productId, skuId, merchantCategoryId, displayName, productType, url, brand, Precio_regular, Precio_Oferta, IdPadre,market) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', 
                                                   (productId, skuId, merchantCategoryId, displayName, productType, url, brand, regular_price, real_price, idSubcategory, _MARKET))
                cur.connection.commit()
                contadorCategory = contadorCategory + 1
                while paginaActual <= cantidadpaginas:
                    #print( ROOT_URL + leaf['link'] + '?page=' + str(paginaActual))
                    webBrowser.get(ROOT_URL + leaf['link'] + '?page=' + str(paginaActual))
                    time.sleep(5)
                    try:
                        valor = webBrowser.execute_script(__NEXT_DATA__)
                    except:
                        valor = ''
                        print('\nSe(2) salta el link '+ ROOT_URL + leaf['link'] + '?page=' + str(paginaActual) + ' por no tener el script NEXT_DATA\n')
                        break

                    datos = json.loads(valor)
                    # Obtiene todos los productos de cada página
                    for props in datos['props']['pageProps']['results']:
                        #print(props['displayName']+'  ' + props['url'])

                        productId = props['productId']
                        skuId = props['skuId']
                        merchantCategoryId = props['merchantCategoryId']
                        displayName = props['displayName']                
                        productType = props['productType']
                        url = props['url'] 
                        try:
                            brand = props['brand']
                        except:
                            brand = 0
                            print('Eror: No se encontró brand en el producId '+ str(productId) )
                        regular_price = props['prices'][0]['price'][0]
                        real_price = props['prices'][0]['price'][0]
                                                                                                                    

                        cur.execute('INSERT INTO productos(productId, skuId, merchantCategoryId, displayName, productType, url, brand, Precio_regular, Precio_Oferta, IdPadre,market) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', 
                                                        (productId, skuId, merchantCategoryId, displayName, productType, url, brand, regular_price, real_price, idSubcategory, _MARKET  ))

                        cur.connection.commit()

                    paginaActual = paginaActual + 1
                #break
            #break
        #break


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
