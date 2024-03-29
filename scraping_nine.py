import requests
from bs4 import BeautifulSoup

class Content:
    """
    Classe-base para todos os artigos/páginas
    """

    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        """
        Uma função flexível de exibição que controla a saída
        """
        print('URL: {}'.format(self.url))
        print('TITLE: {}'.format(self.title))
        print('BODY:\n{}'.format(self.body))

class Website:
    """
    Contém informações sobre a estrutura do site
    """

    def __init__(self, name, url, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.titleTag = titleTag
        self.bodyTag = bodyTag

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
    
    def parse(self, site, url):
        """
        Extrai conteúdo de um dado URL de página
        """
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, site.bodyTag)
            if title != '' and body != '':
                content = Content(url, title, body)
                content.print()

crawler = Crawler()

siteData = [
    ['Globo', 'https://ge.globo.com/',
    'h1.content-head__title', 'p.content-text__container'],
    ['Tecmundo', 'https://www.tecmundo.com.br/',
    'h1#js-article-title', 'div.tec--article__body']
]

#'Salvando' a tag de título, a tag de conteúdo e o link do site para uso futuro
website = []
for row in siteData:
    website.append(Website(row[0], row[1], row[2], row[3]))

#Chamando a função '.parse()' que vai buscar o título e o conteúdo do site de acordo com o primeiro parâmetro... o website.
crawler.parse(website[0], 'https://ge.globo.com/futebol/times/palmeiras/noticia/2024/02/01/'\
                'dudu-denuncia-golpe-de-r-18-milhoes-policia-investiga-ex-braco-direito-do-jogador-do-palmeiras.ghtml')
crawler.parse(website[1], 'https://www.tecmundo.com.br/mercado/'\
              '279376-sumiram-mapa-7-big-techs-deixaram-existir.htm')