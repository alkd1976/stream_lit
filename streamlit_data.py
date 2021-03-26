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
import datapane as dp
import plotly.offline as py
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly_dark"
import streamlit as st
from plotly.subplots import make_subplots
db1 = navfinstratdb.getdb()
to_d = pd.read_sql("SELECT MAX(DATE) as dt FROM intradayoptions.fut1min", db1)['dt'].values[0]
symbols = list(pd.read_sql("SELECT distinct symbol as symbol from intradayoptions.fut1min where date='"+str(to_d)+"' and symbol not like 'NAM%'", db1)['symbol'].values)
st.set_page_config(
    page_title="Intraday/EOD Charts (NSE FNO Stocks)",
    layout="wide")

ticker = st.sidebar.selectbox(
    'Choose a NSE FNO Stock',
     symbols)

i = st.sidebar.selectbox(
        "Interval in minutes",
        ("1m", "3m", "5m", "15m", "30m", "60m", "Daily")
    )
p = st.sidebar.number_input("How many days (1-100)", min_value=1, max_value=100, step=1)

df = pd.read_sql("SELECT datetime, open, high, low, close, volume from intradayoptions.fut1min where symbol = '"+str(ticker)+"' and date(datetime)<='"+str(to_d)+"' and date(datetime)>='"+str(to_d - timedelta(days=p))+"' order by datetime ASC", db1)
if ((i!='1m')|(i!='Daily')):
    df.set_index('datetime', inplace = True)
    df.index = df.index + timedelta(minutes=-1)
if i == '1m':
    per = '1Min'  
    in_t = 1
if i == '3m':
    per = '3Min'  
    in_t = 3
elif i == '5m':
    per = '5Min'
    in_t = 5
elif i == '15m':
    per = '15Min'
    in_t = 15
elif i == "30m":
    per ='30Min'
    in_t = 30
elif i == "60m":
    per = '60Min'
    in_t = 60
elif i == "Daily":
    per = 'D'
else:
    print("Incorrect period chosen for Resampling")
df1 = pd.DataFrame()
df1['open'] = df.open.resample(per).first()
df1['high'] = df.high.resample(per).max()
df1['low'] = df.low.resample(per).min()
df1['close'] = df.close.resample(per).last()
df1['volume'] = df.volume.resample(per).sum()
if i!='Daily':
    df1.index = df1.index + timedelta(minutes=in_t)
df1.dropna(how='any', axis=0, inplace = True)
df = df1.copy()
fig2 = go.Figure(go.Candlestick(x=df.index, open=df.open, high=df.high, low=df.low, close=df.close))
fig2.update_layout(
    xaxis= {
        'type': 'category', 
        'categoryorder': 'category ascending',
        'rangeslider': {'visible': False},
        },
    title={
        'text': str(ticker)+" Stock Price (Candle Stick)",
        'x':0.5,
        'xanchor': 'center'})
#fig2.show()
config={
        'modeBarButtonsToAdd': ['drawline']
    }

st.plotly_chart(fig2, use_container_width=False, config=config)
        
