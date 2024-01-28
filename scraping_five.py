from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re

pages = set()
def getLinks(pageUrl):
    global pages
    try:
        html = urlopen('http://en.wikipedia.org{}'.format(pageUrl))
    except HTTPError as e:
        print('Erro ao buscar o link: http://en.wikipedia.org{}'.format(pageUrl))

    try:
        bs = BeautifulSoup(html, 'html.parser')
        for link in bs.find_all('a', href=re.compile('^(/wiki/)')):
            if 'href' in link.attrs:
                if link.attrs['href'] not in pages:
                    #Encontramos uma página nova
                    newPage = link.attrs['href']
                    print(newPage)
                    pages.add(newPage)
                    getLinks(newPage)
    except AttributeError as e:
        print('Erro ao buscar o conteúdo da página: http://en.wikipedia.org{}'.format(pageUrl))

getLinks('')