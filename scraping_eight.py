from urllib.error import HTTPError
import requests
from bs4 import BeautifulSoup

bs = set()
contentBrookings = set()

class Content:
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

def getPage(url):
    try:
        req = requests.get(url)
    except HTTPError as e:
        print('Erro ao acessar a URL: {}'.format(url))
    
    try:
        bs = BeautifulSoup(req.text, 'html.parser')
    except AttributeError as e:
        print('Erro ao acessar o conteúdo do site: {}'.format(url))

    return bs

def scrapeGlobo(url):
    bs = getPage(url)
    title = bs.find('h1', {'class':'content-head__title'}).text
    lines = bs.find_all('p', {"class":"content-text__container"})
    body = '\n'.join([line.text for line in lines])
    return Content(url, title, body)

def scrapeBrookings(url):
    bs = getPage(url)
    title = bs.find('h1').text
    lines = bs.find_all('div', {'class':'byo-block'})
    body = '\n'.join([line.text for line in lines])
    return Content(url, title, body)

url = 'https://www.brookings.edu/blog/future-development/2018/01/26/delivering-inclusive-urban-access-3-uncomfortable-truths'

content = scrapeBrookings(url)
print('Title: {}'.format(content.title))
print('URL: {}\n'.format(content.url))
print(content.body)

url = 'https://ge.globo.com/mt/futebol/times/cuiaba/noticia/2024/01/30/cuiaba-divulga-imagens-aereas-do-novo-ct-que-viralizam-nas-redes-sociais.ghtml'

content = scrapeGlobo(url)
print('Title: {}'.format(content.title))
print('URL: {}\n'.format(content.url))
print(content.body)