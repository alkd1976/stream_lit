# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 11:54:04 2021

@author: alokk
"""
import pandas as pd
import numpy as np
import datetime
from datetime import date, timedelta, time
import sys
sys.path.append('C:\\Users\\alokk\\Downloads\\pyzipfiles\\Python27\\Zerodha')
sys.path.append("C:\\Users\\alokk\\anaconda3\\Lib\\site-packages\\akdlibraries")
import navfinstratdb
import plotly.figure_factory as ff
import plotly.offline as py
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio
#pio.templates.default = "plotly_dark"
import streamlit as st
from plotly.subplots import make_subplots
from PIL import Image
#img = Image.open("C:/Users/alokk/Downloads/pyzipfiles/Python27/IIFL//qcalpha_logo.jpg")
#st.image(img,width=1200,caption="QCALPHA")
db1 = navfinstratdb.getdb()
dt = datetime.datetime.today().date()
df = pd.read_sql("SELECT * from iifl.altf6 where tradedate ='"+str(dt)+"'", db1)
df['expiry'] = pd.to_datetime(df['expiry']).dt.date
client_list = list(np.unique(df['ClientID']))
strategy_list = list(np.unique(df['strategy']))
series_list = list(np.unique(df['series']))
symbol_list = list(np.unique(df['symbol']))
expiry_list = list(pd.to_datetime(np.unique(df[df['series']!='EQ']['expiry'])).date)

strike_list = list(np.unique(df['strike']))
strike_list.remove(0.0)
option_type_list = list(np.unique(df['option_typ']))
option_type_list.remove('EQ')

df = df.drop(columns=['tradedate', 'strategy_id', 'stream', 'GeneratedBy'])
st.markdown("<h1 style='text-align: center; color: white;'> IIFL AltF+6</h1>", unsafe_allow_html=True)
#st.title("QCALPHA IIFL AltF+6")
#st.image(img, use_column_width=True)
#st.image(img, use_column_width=True)
client_choice = st.sidebar.selectbox(
    'Clients',
     client_list)
df1 = df[df['ClientID']==client_choice]
strategy = np.unique(df[df['ClientID'] == client_choice]['strategy'].values)
strategy_choice = st.sidebar.selectbox('Strategy', strategy) 
df2 = df1[df1['strategy']==strategy_choice]
st.dataframe(df1)
st.dataframe(df2) # will display the dataframe
#st.table(df)# will display the table   
#st.write(df)