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
    
def cincod_news(cincod_entries,word_count=100):
    cincod = {}
    for i in range(len(cincod_entries)):
        noticia = {'newspaper':None,'title':None,'headline':None,'summarise':None,'date':None,'link':None,'text':None,'current_date':None,'img':None,'premium':None,'tag':None}
        # Periodico
        noticia['newspaper'] = find_between(s=cincod_entries[i]['id'], first='//', last='.' )
        # Title
        noticia['title'] = cincod_entries[i]['title']
        # Headline
        headline =  re.sub(pattern='&quot;',repl='"',string=cincod_entries[i]['summary_detail']['value'])
        noticia['headline'] = headline
        # Date
        noticia['date'] = {'date1':cincod_entries[i]['published'],'date2':cincod_entries[i]['published_parsed']}
        # Link
        noticia['link'] = cincod_entries[i]['id']
        # Text
        text = get_only_text(cincod_entries[i]['id'])[0]
        if text.find('»') != -1:
            index = get_only_text(cincod_entries[i]['id'])[0].index('»') +3
            text = get_only_text(cincod_entries[i]['id'])[0][index:]
        noticia['text'] = text
        # Bank Tags
        noticia['tag'] = bank_tags(text)
        # Summarise
        noticia['summarise'] = summarize(text, word_count=word_count)        
        # Current Date
        noticia['current_date'] = datetime.datetime.now().timetuple()
        # Image
        if len(cincod_entries[i]['links']) > 1:
            noticia['img'] = cincod_entries[i]['links'][1]['href']
        else:
             noticia['img'] = None
        cincod.update({'Noticia'+'_'+str("%02d")%(i+1):noticia})
    return cincod

# Entries
print('Cargando Entradas')
url_cinco_dias = 'https://cincodias.elpais.com/seccion/rss/companias/'
cincod = feedparser.parse(url_cinco_dias)
cincod_entries = cincod['entries']

# Dict
print('Desarrollando Diccionario')
cincod = cincod_news(cincod_entries,word_count=100)

# Save
print('Guardando Archivo Cinco Días')
with open('../data/data_cincodias.json', 'w') as fp:
    json.dump(cincod, fp)
# Load 
jsonFile = open("../data/data.json", "r")
data = json.load(jsonFile)
data["cincodias"] = cincod
# Save
print('Guardando Archivo General')
with open('../data/data.json', 'w') as fp:
    json.dump(data, fp)