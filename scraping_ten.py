import requests
from bs4 import BeautifulSoup

class Content:
    """
    Classe-base para todos os artigos/páginas
    """

    def __init__(self, url, title, body, topic):
        self.url = url
        self.title = title
        self.body = body
        self.topic = topic

    def print(self):
        """
        Uma função flexível de exibição que controla a saída
        """
        print('URL: {}'.format(self.url))
        print('TOPIC: {}'.format(self.topic))
        print('TITLE: {}'.format(self.title))
        print('BODY:\n{}'.format(self.body))

class Website:
    """
    Contém informações sobre a estrutura do site
    """

    def __init__(self, name, url, titleTag, bodyTag, searchUrl, resultListing, resultUrl, absoluteUrl):
        self.name = name
        self.url = url
        self.titleTag = titleTag
        self.bodyTag = bodyTag
        self.searchUrl = searchUrl
        self.resultListing = resultListing
        self.resultUrl = resultUrl
        self.absoluteUrl = absoluteUrl

class Crawler:
    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return print('Erro ao buscar o conteúdo da url: {}'.format(url))
        return BeautifulSoup(req.text, 'html.parser')
    
    def safeGet(self, pageObj, selector):
        """
        Procura o título e o conteúdo princípal de um site pelo - que é o 'pageObj' que virá.
        """
        selectedElems = pageObj.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return '\n'.join(
                [elem.get_text() for elem in selectedElems])
        return ''
    
    def search(self, topic, site):
        """
        Pesquisa um dado site em busca de um dado tópico e registra todas as páginas encontradas
        """
        bs = self.getPage(site.searchUrl + topic)
        searchResults = bs.select(site.resultListing)
        for result in searchResults:
            url = result.select(site.resultUrl)[0].find('a').attrs['href']
            #Verifica se é um URL relativo ou absoluto
            if(site.absoluteUrl):
                bs = self.getPage(url)
            else:
                bs = self.getPage(site.url + url)
            if bs is None:
                print('Erro ao acessar o conteúdo da URL: {}'.format(site.searchUrl + topic))
                return
            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, site.bodyTag)
            if title != '' and body != '':
                content = Content(topic, title, body, url)
                content.print()

crawler = Crawler()

siteData = [
    ['Globo', 'https://ge.globo.com/',
    'h1.content-head__title', 'p.content-text__container',
    'https://ge.globo.com/busca/?q=', 'ul.results__list',
    'div.widget--info__media-container', True]
]

#'Salvando' a tag de título, a tag de conteúdo e o link do site para uso futuro
sites = []
for row in siteData:
    sites.append(Website(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

topics = ['Brasil']
for topic in topics:
    print('GETTING INFO ABOUT: {}'.format(topic))
    for targetSite in sites:
        crawler.search(topic, targetSite)