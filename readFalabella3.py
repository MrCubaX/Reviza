from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
import json
import pymysql

ROOT_URL = 'https://www.falabella.com.pe/falabella-pe'
TAXONOMY_FALABELLA_URL = 'https://www.falabella.com/s/content/v1/taxonomy/pe'

HOST_BBDD = 'localhost'
PORT_BBDD = 3306
USER_BBDD = 'root'
PASS_BBDD = 'mabeliux14'
NAME_BBDD = 'reviza'

connToMysql = pymysql.connect(host = HOST_BBDD ,
                              port = PORT_BBDD,
                              user = USER_BBDD,
                              passwd = PASS_BBDD,
                              db = NAME_BBDD)

optionsOfWeBrowser = webdriver.ChromeOptions()
optionsOfWeBrowser.add_experimental_option(
                        "excludeSwitches",
                        ["enable-logging"])
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
        cur.execute('INSERT INTO categorias (name, description) VALUES (%s, %s)', (categories['label'],categories['link']) )
        cur.connection.commit()
        for subcategorias in categories['subCategories']:
            # #browseIntoSite( ROOT_URL + subcategorias['link'])
            # webBrowser.get(ROOT_URL + subcategorias['link'])
            # time.sleep(28)
            # print(ROOT_URL + subcategorias['link'])
            # numberOfPages = 10            
            # #numberOfPages = webBrowser.find_element_by_class_name('jsx-1738323148 jsx-1104282991 pagination-button')
            # print(numberOfPages)
            # pageSource = webBrowser.page_source
            # pageSourceParse = BeautifulSoup(pageSource,'html.parser')
            # contador = 0
            # print(pageSourceParse)
            # for productosList in pageSourceParse.findAll(name='div', attrs={'class':'jsx-1395131234 search-results-4-grid'} ):#attrs={'class':'jsx-3686231685 product-name fa--product-name'}):
            #     #print('Título del producto: ' + productosList.get_text() )                
            #     contador = contador + 1
            #     print(contador)
            #     #time.sleep(5)
            cantidadpaginas = 1
            paginaActual = 1
            for leaf in subcategorias['leafCategories']:                

                print('                '+ leaf['link']+ '?page=1'  )
                webBrowser.get(ROOT_URL + leaf['link'] + '?page=1'  )
                time.sleep(5)
                valor = webBrowser.execute_script('return document.getElementById("__NEXT_DATA__").innerHTML')
                datos = json.loads(valor)
                contador =datos['props']['pageProps']['pagination']['count']
                porPagina = datos['props']['pageProps']['pagination']['perPage']
                print('contador es: '+  str(contador))
                print('Por pagina es:'+ str(porPagina))
                cantidadpaginas = round(int(contador) / int(porPagina))
                cantidadpaginas2 = cantidadpaginas * porPagina

                if cantidadpaginas2 < contador:
                    cantidadpaginas = cantidadpaginas + 1

                print(cantidadpaginas)
                
                while paginaActual <= cantidadpaginas:
                    
                # for props in datos['props']['pageProps']['pagination']:
                #     print(props['count'])
                #     print(props['perPage'])
                #     cantidadpaginas = round(int(props['count']) / int(props['perPage']))
                #     print(cantidadpaginas)
                    print('                '+ leaf['link']+ '?page=' + str(paginaActual)  )
                    webBrowser.get(ROOT_URL + leaf['link'] + '?page=' + str(paginaActual) )
                    time.sleep(15)
                    valor = webBrowser.execute_script('return document.getElementById("__NEXT_DATA__").innerHTML')
                    datos = json.loads(valor)
                    #Obtiene todos los productos de cada página
                    for props in datos['props']['pageProps']['results']:
                        print(props['displayName']+'  '+ props['url'])

                    paginaActual = paginaActual +1
                break
            break
        break





def browseIntoSite(urlSiteToVisit):
    webBrowser.get(urlSiteToVisit)
    numberOfPages = webBrowser.find_element_by_class_name('jsx-1738323148 jsx-1104282991 pagination-button').value
    print(numberOfPages)
    pageSource = webdriver.page_source
    pageSourceParse = BeautifulSoup(pageSource,'html.parser')
    for productosList in pageSourceParse.findAll(name='div', attrs={'class':'jsx-3686231685 product-name fa--product-name'}):
        print('Título del producto: ' + productosList.get_text() )




cur = connToMysql.cursor()
cur.execute('USE reviza')

getLinksOfMenu()
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

#getLinksOfWeb()


def visitLinksOfWeb(linksJSON):
    print('')

def getJSONOfWeb(url):
    print('')

def getNumberOfPages(jsonString):
    print('')

