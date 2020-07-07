import streamlit as st
import json
import webbrowser

#### CSS Style ####
with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

#### Functions ####
def show_news(news,key):
    st.image('./img/expansion2.png',format='PNG')
    st.markdown('####'+' '+news['title'])
    st.markdown(news['date']['date1'])
    st.markdown('##### Headline')
    st.markdown(news['headline'])
    st.markdown('##### Summarise')
    st.markdown(news['summarise'])
    st.image(news['img'],width=400)
    if st.button('Link',key=key):
        webbrowser.open(news['link'])

#### Data ####
# Load 
jsonFile = open("./data/data.json", "r")
data = json.load(jsonFile)

news = data['expansion']['Noticia_01']

def main():
    # Front Image
    url = './img/img2.png'
    st.image(url,use_column_width=True)
    # Dashboard Title
    st.markdown('# NEWSSTAND PROJECT')

    for k,news in data['expansion'].items():
        show_news(news,key=k)

if __name__ == "__main__":
    main()