from urllib.request import urlopen
from urllib.request import HTTPError
from bs4 import BeautifulSoup
import random
import re

def getLinks(articleUrl):
    try:
        html = urlopen('http://en.wikipedia.org{}'.format(articleUrl))
    except HTTPError as e:
        return print('Erro ao buscar o link enviado: {}'.format(e))
    
    try:
        bs = BeautifulSoup(html, 'html.parser')
        return bs.find('div', {'id':'bodyContent'}).find_all('a',
            href=re.compile('^(/wiki/((?!:).)*$)'))
    except AttributeError as e:
        print('Erro ao buscar o conteúdo da página: {}'.format(e))

links = getLinks('/wiki/Kevin_Bacon')
while len(links) > 0:
    newArticle = links[random.randint(0, len(links)-1)].attrs['href']
    print(newArticle)
    links = getLinks(newArticle)