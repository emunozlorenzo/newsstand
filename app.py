import streamlit as st
import json
import webbrowser

#### CSS Style ####
with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

#### Functions ####
def show_news(news,key,newspaper):
    st.image('./img/'+newspaper+'.png',format='PNG')
    st.markdown('####'+' '+news['title'])
    st.markdown(news['date']['date1'])
    st.markdown('##### Headline')
    st.markdown(news['headline'])
    st.markdown('##### Summarise')
    st.markdown(news['summarise'])
    if newspaper == 'expansion':
        st.image(news['img'],width=400)
    if st.button('Link',key=key):
        webbrowser.open(news['link'])
    st.markdown('\n')

#### Data ####
# Load 
jsonFile = open("./data/data.json", "r")
data = json.load(jsonFile)

def main():
    # Front Image
    url = './img/img2.png'
    st.image(url,use_column_width=True)
    # Dashboard Title
    st.markdown('# NEWSSTAND PROJECT')
    # Selectbox
    options = [i.capitalize() for i in list(data.keys())]
    newspaper = st.selectbox(label='Select Newspaper', options=options, index=0, key='newspaper_select_box')
    # News
    for k,news in data[newspaper.lower()].items():
        show_news(news,key=k,newspaper=newspaper.lower())

if __name__ == "__main__":
    main()