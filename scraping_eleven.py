class Website:
    """Classe-base comum para todos os artigos/páginas"""

    def __init__(self, type, name, url, searchUrl, resultListing,
                 resultUrl, absoluteUrl, titleTag, bodyTag, pageType):
        self.name = name
        self.url = url
        self.titleTag = titleTag
        self.bodyTag = bodyTag
        self.pageType = pageType

class Webpage:
    """Classe-base comum para todos os artigos/páginas"""

    def __init__(self, name, url, titleTag):
        self.name = name
        self.url = url
        self.titleTag = titleTag

class Product(Website):
    """Contém informações para coletar dados de uma página de produto"""

    def __init__(self, name, url, titleTag, productNumber, price):
        Website.__init__(self, name, url, titleTag)
        self.productNumber = productNumber
        self.price = price

class Article(Website):
    """Contém informações para coletar dados de uma página de artigo"""

    def __init__(self, name, url, titleTag, bodyTag, dateTag):
        Website.__init__(self, name, url, titleTag)
        self.bodyTag = bodyTag
        self.dateTag = dateTag