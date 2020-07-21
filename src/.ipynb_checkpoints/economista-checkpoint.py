# Libraries
import feedparser
from gensim.summarization.summarizer import summarize
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import re
import json

# Functions
def get_only_text(url):
    
    """
    return the title and the text of the article at the 
    specified url
    """
    
    page=urlopen(url)
    soup=BeautifulSoup(page,"html.parser")
    text=' '.join(map(lambda p: p.text, soup.find_all('p')))
    return [text,soup.title.text]

def get_img(url):
    page=urlopen(url)
    soup=BeautifulSoup(page,"html.parser")
    if soup.find('div',class_='articleHero') != None:
        if soup.find('div',class_='articleHero').find('div',class_='articleImage') != None:
            return soup.find('div',class_='articleHero').find('div',class_='articleImage').find('img')['data-src']
        else: None
    else:
        return None

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def string_found(string1, string2):
    
    if re.search(r"\b" + re.escape(string1) + r"\b", string2.lower()):
        return True
    return False     
    
def bank_tags(text):
    tags = []
    dict_banks = {'Santander':['santander'],'BBVA':['bbva'],'Bankinter':['bankinter'],'Bankia':['bankia'],
                 'Sabadell':['sabadell'],'ING':['ing'],'Abanca':['abanca'],'Deutsche Bank':['deutsche'],
                  'CaixaBank':['caixabank'],'Openbank':['openbank']}
    for key,values in dict_banks.items():
        for i in values:
            if string_found(i,text.lower()):
                tags.append(key)
                break
    return tags
    
def economista_news(economista_entries):
    economista = {}
    for i in range(len(economista_entries)):
        noticia = {'newspaper':None,'title':None,'headline':None,'summarise':None,'summarise_short':None,'summarise_long':None,'date':None,'link':None,'text':None,'current_date':None,'img':None,'premium':None,'tag':None}
        # Periodico
        noticia['newspaper'] = find_between(s=economista_entries[i]['id'], first='www.el', last='.' )
        # Title
        noticia['title'] = economista_entries[i]['title']
        # Headline
        headline =  re.sub(pattern='&quot;',repl='"',string=economista_entries[i]['summary_detail']['value'])
        noticia['headline'] = headline
        # Date
        noticia['date'] = {'date1':economista_entries[i]['published'],'date2':economista_entries[i]['published_parsed']}
        # Link
        noticia['link'] = economista_entries[i]['id']
        # Text
        text = get_only_text(economista_entries[i]['id'])[0][len(headline)+1:]
        if  text.find('\n\t\t\t\tif') != -1:
            index =  text.find('\n\t\t\t\tif')
            text = text[:index]
        noticia['text'] = text
        # Bank Tags
        noticia['tag'] = bank_tags(text)
        # Summarise
        noticia['summarise'] = summarize(text, word_count=100)
        noticia['summarise_short'] = summarize(text, word_count=50) 
        noticia['summarise_long'] = summarize(text, word_count=200) 
        # Current Date
        noticia['current_date'] = datetime.datetime.now().timetuple()
        # Image
        noticia['img'] = get_img(economista_entries[i]['id'])
        economista.update({'Noticia'+'_'+str("%02d")%(i+1):noticia})
    return economista

# Entries
print('Cargando Entradas')
url_economista = 'https://www.eleconomista.es/rss/rss-empresas.php'
economista = feedparser.parse(url_economista)
economista_entries = economista['entries']

# Dict
print('Desarrollando Diccionario')
economista = economista_news(economista_entries)

# Save
print('Guardando Archivo Expansión')
with open('../data/data_economista.json', 'w') as fp:
    json.dump(economista, fp)
# Load 
jsonFile = open("../data/data.json", "r")
data = json.load(jsonFile)
data["economista"] = economista
# Save
print('Guardando Archivo General')
with open('../data/data.json', 'w') as fp:
    json.dump(data, fp)