import streamlit as st
import json
import webbrowser
import datetime
from termcolor import colored
import os

#### CSS Style ####
with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
    st.markdown('<style>h1{color: #043263 ;text-align:center;font-family: Bebas Neue}</style>', unsafe_allow_html=True)
    st.markdown('<style>h3{color: #004481;}</style>', unsafe_allow_html=True)
    st.markdown('<style>h4{color: #1464A5 ;}</style>', unsafe_allow_html=True)
    st.markdown('<style>h2{color: #1464A5 ;}</style>', unsafe_allow_html=True)
    st.markdown('<style>h6{color: #DA3851  ;}</style>', unsafe_allow_html=True)
    
#### Functions ####
def show_news(news,key,newspaper):
    st.image('./img/'+newspaper+'.png',format='PNG')
    st.markdown('###'+' '+news['title'])
    news_date = datetime.datetime(news['date']['date2'][0],news['date']['date2'][1],news['date']['date2'][2],news['date']['date2'][3],news['date']['date2'][4])
    st.markdown(news_date.strftime("%d/%m/%Y, %H:%M"))
    st.markdown('#### Headline')
    st.markdown(news['headline'])
    st.markdown('#### Summarise')
    if news['summarise'] == 'Premium Content':
        st.markdown('######'+' '+news['summarise'])
    else:
        st.markdown(news['summarise'])
    if news['img'] != None:
        st.image(news['img'],width=450,use_column_width=True)
    #if st.button('Link',key=key):
        #webbrowser.open(news['link'])
    st.markdown('**[Link]('+news["link"]+')**')
    st.markdown('\n')

#### Data ####
# Load News
jsonFile = open("./data/data.json", "r")
data = json.load(jsonFile)
# Load Banks
jsonFile2 = open("./data/bank_dict.json", "r")
bank_dict = json.load(jsonFile2)
bank_list = [None] + sorted(list(bank_dict.keys()))

def main():
    # Front Image
    url = './img/img3.png'
    st.image(url,use_column_width=True)
    
    # Dashboard Title
    st.markdown('# FINANCIAL NEWS')
    
    # Sidebar
    banks = st.sidebar.selectbox("Select a bank", options=bank_list,index=0,key='bank_select_box')

    # Update
    if st.button('Update News',key='update'):
        st.write('Coming Soon...')
        #exec(open("./src/expansion.py").read())
        #exec(open("./src/economista.py").read())
    
    # Selectbox
    options = [i.capitalize() for i in list(data.keys())] + ['All']
    newspaper = st.selectbox(label='Select Newspaper', options=options, index=0, key='newspaper_select_box')
    
    # News
    if newspaper == 'All':
        newspapers = list(data.keys())
        dates = []
        for newspaper in newspapers:
            dates_ = [datetime.date(data[newspaper.lower()][i]['date']['date2'][:3][0], data[newspaper.lower()][i]['date']['date2'][:3][1], data[newspaper.lower()][i]['date']['date2'][:3][2]) for i in data[newspaper.lower()]]
            dates = dates + dates_
    else:
        newspapers = [newspaper]
        dates = [datetime.date(data[newspaper.lower()][i]['date']['date2'][:3][0], data[newspaper.lower()][i]['date']['date2'][:3][1], data[newspaper.lower()][i]['date']['date2'][:3][2]) for i in data[newspaper.lower()]]
    
    # Dates
    max_date = max(d for d in dates if isinstance(d, datetime.date))
    min_date = min(d for d in dates if isinstance(d, datetime.date))
    d = st.date_input("Select Date",value=max_date, min_value=min_date, max_value=max_date)

    for newspaper in newspapers:
        for k,news in data[newspaper.lower()].items():
            if datetime.date(news['date']['date2'][:3][0], news['date']['date2'][:3][1], news['date']['date2'][:3][2]) == d:
                if banks == None:
                    show_news(news,key=k,newspaper=newspaper.lower())
                elif banks in news['tag']:
                    show_news(news,key=k,newspaper=newspaper.lower())

if __name__ == "__main__":
    main()