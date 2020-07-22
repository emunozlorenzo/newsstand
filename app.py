import streamlit as st
import json
import webbrowser
import datetime
from termcolor import colored
import os
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
import pickle
import yfinance as yf
import altair as alt
import numpy as np
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure

#### CSS STYLE ####
with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
    st.markdown('<style>h1{color: #043263 ;text-align:center;font-family: Bebas Neue}</style>', unsafe_allow_html=True)
    st.markdown('<style>h3{color: #004481;}</style>', unsafe_allow_html=True)
    st.markdown('<style>h4{color: #1464A5 ;}</style>', unsafe_allow_html=True)
    st.markdown('<style>h2{color: #1464A5 ;}</style>', unsafe_allow_html=True)
    st.markdown('<style>h6{color: #DA3851  ;}</style>', unsafe_allow_html=True)
    
#### FUNCTIONS ####
def show_news(news,key,newspaper,summarise):
    st.image('./img/'+newspaper+'.png',format='PNG')
    st.markdown('###'+' '+news['title'])
    news_date = datetime.datetime(news['date']['date2'][0],news['date']['date2'][1],news['date']['date2'][2],news['date']['date2'][3],news['date']['date2'][4])
    st.markdown(news_date.strftime("%d/%m/%Y, %H:%M"))
    st.markdown('#### Headline')
    st.markdown(news['headline'])
    st.markdown('#### Summary')
    if news[summarise] == 'Premium Content':
        st.markdown('######'+' '+news[summarise])
    else:
        st.markdown(news[summarise])
    if news['img'] != None:
        st.image(news['img'],width=450,use_column_width=True)
    #if st.button('Link',key=key):
        #webbrowser.open(news['link'])
    st.markdown('**[Link]('+news["link"]+')**')
    st.markdown('\n')

def datetime_(x):
    return np.array(x, dtype=np.datetime64)

def plot_yf(code,company_name,period):
    company = yf.Ticker(code)
    hist = company.history(period=period)
    close = hist[['Close','Volume']]
    # Graphs
    #st.line_chart(close[['Close']],height=200)
    #c = alt.Chart(close.reset_index()).mark_line().encode(x='Date',y='Close',tooltip=['Date', 'Close'])
    #st.altair_chart(c, use_container_width=True)
    close['Date'] = pd.to_datetime(close.index, format='%Y-%m-%d')
    close["DateString"] = close["Date"].dt.strftime("%Y-%m-%d")
    source = ColumnDataSource(data={
        'date'      : close['Date'],
        'adj close' : close['Close'],
        'volume'    : close['Volume'],
    })
    p = figure(plot_height=250, x_axis_type="datetime", tools="", toolbar_location=None,
               title=company_name, sizing_mode="scale_width")
    p.background_fill_color="#f5f5f5"
    p.grid.grid_line_color="white"
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    p.axis.axis_line_color = None
    p.line(x='date', y='adj close', line_width=2, color='#16D29B', source=source)
    p.add_tools(HoverTool(
        tooltips=[
            #( 'date',   '@date{F%}'            ),
            ( 'close',  '@{adj close}{0.00 a}€' ), # use @{ } for field names with spaces
            ( 'volume', '@volume{0.00 a}'      ),
        ],

        formatters={
            'date'      : 'datetime', # use 'datetime' formatter for 'date' field
            'adj close' : 'printf',   # use 'printf' formatter for 'adj close' field
                                    # use default 'numeral' formatter for other fields
        },

        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode='vline'
    ))
    return st.bokeh_chart(p, use_container_width=True)

#### DATA ####
# Load News
jsonFile = open("./data/data.json", "r")
data = json.load(jsonFile)
# Load Banks
jsonFile2 = open("./data/bank_dict.json", "r")
bank_dict = json.load(jsonFile2)
bank_list = [None] + sorted(list(bank_dict.keys()))
dict_yf = {'BBVA':'BBVA.MC','Santander':'SAN.MC','Sabadell':'SAB.MC',
'CaixaBank':'CABK.MC','Bankinter':'BKT.MC','Bankia':'BKIA.MC','ING':'ING',
'Deutsche Bank':'DBK.DE','Openbank':None,'Abanca':None}
dict_ibex35 = {'CaixaBank':'CABK.MC','Bankia':'BKIA.MC','Sabadell':'SAB.MC','Bankinter':'BKT.MC','BBVA':'BBVA.MC','Santander':'SAN.MC',
'ENCE':'ENC.MC','AENA':'AENA.MC','Iberdrola':'IBE.MC','Enagas':'ENG.MC',
'Inmobiliaria Colonial':'COL.MC','ACS':'ACS.MC','Viscofan':'VIS.MC',
'Amadeus':'AMS.MC','Endesa':'ELE.MC','Siemens Gamesa':'SGRE.MC','Red Eléctrica':'REE.MC',
'ArcelorMittal':'MTS.MC','Telefonica':'TEF.MC','Acciona':'ANA.MC','Cellnex':'CLNX.MC',
'MERLIN Properties':'MRL.MC','Ferrovial':'FER.MC','Naturgy':'NTGY.MC',
'Mediaset':'TL5.MC','INDITEX':'ITX.MC','Grifols':'GRF.MC','IAG':'IAG.MC',
'Melia':'MEL.MC'}
periods = ['1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max']
# Mask
bank_mask = np.array(Image.open("./img/bank4.png"))
# Stopwords
with open("./data/stopwords.txt", "rb") as fp:   # Unpickling
    stopwords = pickle.load(fp)

#### APP ####
def main():
    #### MAIN SIDEBAR ####
    st.sidebar.markdown('## NEWSSTAND PROJECT')
    # Navigation
    st.sidebar.markdown('### Navigation')
    page = st.sidebar.selectbox("Choose a page", ['NEWSSTAND', 'IBEX35'])
    #### END SIDEBAR ####
    
    #### PAGE 1 ####
    if page == 'NEWSSTAND':
        #### Sidebar PAGE 1 ####
        # Banks
        st.sidebar.markdown('### Bank')
        banks = st.sidebar.selectbox("Select a bank", options=bank_list,index=0,key='bank_select_box')
        # Sumary
        st.sidebar.markdown('### Summary')
        summary = st.sidebar.radio(label='Select a type of Summary', options=['Short','Medium','Large'], index=1, key='radio-summarise')
        if summary == 'Short':
            summarise = 'summarise_short'
        elif summary == 'Medium':
            summarise = 'summarise'
        else:
            summarise = 'summarise_long'
        #### End Sidebar PAGE 1 ####
        
        # Front Image
        url = './img/img4.png'
        st.image(url,use_column_width=True)
        # Dashboard Title
        if banks != None:
            if dict_yf[banks] != None:
                st.markdown('###'+' '+banks)
                period = st.selectbox(label='Select Period', options=periods, index=5, key='stock_select_box')
                plot_yf(code=dict_yf[banks],company_name=banks,period=period)

        # Selectbox
        options = [i.capitalize() for i in list(data.keys())] + ['All']
        newspaper = st.selectbox(label='Select Newspaper', options=options, index=3, key='newspaper_select_box')
        
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

        text_list = []
        for newspaper in newspapers:
            for k,news in data[newspaper.lower()].items():
                if datetime.date(news['date']['date2'][:3][0], news['date']['date2'][:3][1], news['date']['date2'][:3][2]) == d:
                    if banks == None:
                        show_news(news,key=k,newspaper=newspaper.lower(),summarise=summarise)
                    elif banks in news['tag']:
                        show_news(news,key=k,newspaper=newspaper.lower(),summarise=summarise)
                        text_list.append(news['text'])

    #   if len(text_list) > 0:
    #       text_list_string = " ".join(text_list)
    #       # Create and generate a word cloud image:
    #       wordcloud = WordCloud(width=400,height=400,margin=1,
    #                      background_color='white',mask=bank_mask,stopwords=stopwords).generate(text_list_string)
    #
    #        # Display the generated image:
    #        fig = plt.figure(figsize = (40,40))
    #        fig.patch.set_facecolor('black')
    #        plt.imshow(wordcloud, interpolation='bilinear')
    #        plt.axis("off")
    #        plt.show()
    #        st.sidebar.pyplot()

    #### PAGE 2 ####
    elif page == 'IBEX35':
        # Front Image
        url = './img/img6.png'
        st.image(url,use_column_width=True)
        companies = st.selectbox("Select a Company", options=sorted(list(dict_ibex35.keys())),index=0,key='companies_select_box')
        period_ = st.selectbox(label='Select Period', options=periods, index=5, key='stock_select_box2')
        plot_yf(code=dict_ibex35[companies],company_name=companies,period=period_)

if __name__ == "__main__":
    main()