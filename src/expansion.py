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
    # Eliminar Última Hora
    rest = soup.find_all('p', attrs={'class' : "line-clamp_x2 ue-c-widget__article-headline"})[0].text
    index = text.find(rest)
    final_text = text[:index]
    return [final_text,soup.title.text]

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
    
def expansion_news(expansion_entries,word_count=100):
    expansion = {}
    for i in range(len(expansion_entries)):
        noticia = {'newspaper':None,'title':None,'headline':None,'summarise':None,'date':None,'link':None,'text':None,'current_date':None,'img':None,'premium':None}
        # Periodico
        noticia['newspaper'] = find_between(s=expansion_entries[i]['id'], first='www.', last='.' )
        # Title
        noticia['title'] = expansion_entries[i]['title']
        # Headline
        index = expansion_entries[i]['summary_detail']['value'].find('&nbsp')
        if index != -1:
            noticia['headline'] = expansion_entries[i]['summary_detail']['value'][:index]
        else:
            noticia['headline'] = re.sub(pattern='&quot;',repl='"',string=expansion_entries[i]['summary_detail']['value'])
        # Date
        noticia['date'] = {'date1':expansion_entries[i]['published'],'date2':expansion_entries[i]['published_parsed']}
        # Link
        noticia['link'] = expansion_entries[i]['id']
        # Text
        text = get_only_text(expansion_entries[i]['id'])[0]
        noticia['text'] = text
        # Summarise
        if text.find('Para seguir leyendo') == -1:
            noticia['summarise'] = summarize(text, word_count=word_count)
            noticia['premium'] = False
        else:
            noticia['summarise'] = 'Premium Content'
            noticia['premium'] = True
        # Current Date
        noticia['current_date'] = datetime.datetime.now().timetuple()
        # Image
        noticia['img'] = expansion_entries[i]['media_content'][0]['url']
        expansion.update({'Noticia'+'_'+str("%02d")%(i+1):noticia})
    return expansion

# Entries
print('Cargando Entradas')
url_expansion = 'https://e00-expansion.uecdn.es/rss/empresasbanca.xml'
expansion = feedparser.parse(url_expansion)
expansion_entries = expansion['entries']

# Dict
print('Desarrollando Diccionario')
expansion = expansion_news(expansion_entries,word_count=100)

# Save
print('Guardando Archivo Expansión')
with open('../data/data_expansion.json', 'w') as fp:
    json.dump(expansion, fp)
# Load 
jsonFile = open("../data/data.json", "r")
data = json.load(jsonFile)
data["expansion"] = expansion
# Save
print('Guardando Archivo General')
with open('../data/data.json', 'w') as fp:
    json.dump(data, fp)