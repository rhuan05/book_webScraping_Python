from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import random

pages = set()

#Obtém uma lista de todos os links internos encontrados em uma página
def getInternalLinks(bs, includeUrl):
    includeUrl = '{}://{}'.format(urlparse(includeUrl).scheme, urlparse(includeUrl).netloc)
    internalLinks = []
    #Encontra todos os links que começam com '/'
    for link in bs.find_all('a', href=re.compile('^(/|.*'+includeUrl+')')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                if(link.attrs['href'].startswith('/')):
                    internalLinks.append(includeUrl+link.attrs['href'])
                else:
                    internalLinks.append(link.attrs['href'])
    return internalLinks

#Obtém uma lista de todos os links externos encontrados em uma página
def getExternalLinks(bs, excludeUrl):
    externalLinks = []
    #Encontra todos os links que começam com 'http' e que
    #não contenham o URL atual
    for link in bs.find_all('a', href=re.compile('^(http|www)((?!'+excludeUrl+').)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks

def getRandomExternalLink(startingPage):
    try:
        html = urlopen(startingPage)
    except HTTPError as e:
        print('Erro ao buscar o link: {}'.format(startingPage))

    try:
        bs = BeautifulSoup(html, 'html.parser')
    except AttributeError as e:
        print('Erro ao buscar o link: {}'.format(startingPage))
        
    externalLinks = getExternalLinks(bs, urlparse(startingPage).netloc)
    if len(externalLinks) == 0:
        print('No external links, looking around the site for one')
        domain = '{}://{}'.format(urlparse(startingPage).scheme, urlparse(startingPage).netloc)
        internalLinks = getInternalLinks(bs, domain)
        return getRandomExternalLink(internalLinks[random.randint(0, len(internalLinks)-1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks)-1)]
    
#Coleta de uma lista de todos os URLs externos encontrados no site
allExtLinks = set()
allIntLinks = set()

def getAllExternalLinks(siteUrl):
    try:
        html = urlopen(siteUrl)
    except HTTPError as e:
        print('Erro ao buscar o link: {}'.format(siteUrl))
        
    domain = '{}://{}'.format(urlparse(siteUrl).scheme, urlparse(siteUrl).netloc)
    try:
        bs = BeautifulSoup(html, 'html.parser')
    except AttributeError as e:
        print('Erro ao buscar o link: {}'.format(siteUrl))
    
    internalLinks = getInternalLinks(bs, domain)
    externalLinks = getExternalLinks(bs, domain)

    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            print('Link externo: ' + link)

    for link in internalLinks:
        if link not in allIntLinks:
            allIntLinks.add(link)
            print('Link interno: ' + link)

    allIntLinks.add('http://oreilly.com')
    getAllExternalLinks('http://oreilly.com')

    
def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    print('Random external link is: {}'.format(externalLink))
    followExternalOnly(externalLink)

followExternalOnly('http://oreilly.com')