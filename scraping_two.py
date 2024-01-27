from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen('https://en.wikipedia.org/wiki/Cristiano_Ronaldo')
bs = BeautifulSoup(html, 'html.parser')

for time in bs.find_all('a'):
    print(time.attrs['href'])