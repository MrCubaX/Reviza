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
webBrowser = webdriver.Chrome(
                            options=optionsOfWeBrowser, 
                            executable_path='drivers/chromedriver/chromedriver.exe')


webBrowser.get(TAXONOMY_FALABELLA_URL)
taxonomyOfWeb = webBrowser.find_element_by_tag_name('pre').text

def readJSON():
    data = json.loads(taxonomyOfWeb)
    for categories in data['state']['rootCategories']:
        cur.execute('INSERT INTO categorias (name, description) VALUES (%s, %s)', (categories['label'],categories['link']) )
        cur.connection.commit()
        for subcategorias in categories['subCategories']:
            #browseIntoSite( ROOT_URL + subcategorias['link'])
            webBrowser.get(ROOT_URL + subcategorias['link'])
            time.sleep(2)
            print(ROOT_URL + subcategorias['link'])
            numberOfPages = 10            
            #numberOfPages = webBrowser.find_element_by_class_name('jsx-1738323148 jsx-1104282991 pagination-button')
            datos = webBrowser.find_element_by_id('__NEXT_DATA__')
            print(datos.text )
            print(numberOfPages)
            valor = webBrowser.execute_script('return document.getElementById("__NEXT_DATA__").innerHTML')
            print(valor)

            pageSource = webBrowser.page_source
            pageSourceParse = BeautifulSoup(pageSource,'html.parser')
            contador = 0
            #print(pageSourceParse)
            for productosList in pageSourceParse.findAll(name='script', attrs={'id':'__NEXT_DATA__'} ):#attrs={'class':'jsx-3686231685 product-name fa--product-name'}):
                print('Título del producto: ' + productosList.get_text() )                
                contador = contador + 1
                print(contador)
                #time.sleep(5)
        #     for leaf in subcategorias['leafCategories']:
        #         print('                '+ leaf['lirnk'])
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


readJSON()
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
