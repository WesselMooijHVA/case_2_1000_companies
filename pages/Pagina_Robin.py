import requests
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import authentication

api = KaggleApi()

authentication.auth_json(api)

api.dataset_download_files('surajjha101/fortune-top-1000-companies-by-revenue-2022', unzip=True)
df_2022 = pd.read_csv('Fortune 1000 Companies by Revenue.csv')

api.dataset_download_files('shivamb/fortune-global-2000-companies-till-2021', unzip=True)
df_2021 = pd.read_csv('fortune_2000_in_2021.csv')


df_2021 = df_2021.rename(columns={'Rank':'Rank 2021', 'Sales':'Sales 2021', 'Profit':'Profit 2021', 'Assets':'Assets 2021', 'Market Value':'Market Value 2021'})
df_2022 = df_2022.rename(columns={'rank ':'Rank 2022', 'name ':'Name', 'revenues ':'Revenues 2022', 'profits ':'Profits 2022', 'assets':'Assets 2022', 'market_value ':'Market Value 2022', 'employees ':'Employees'})

df_2022 = df_2022.join(df_2021.set_index('Name'), on='Name')


#clean up strings
col_convert = [ 'Revenues 2022', 'Profits 2022', 'Assets 2022', 'Market Value 2022', 'revenue_percent_change', 'profits_percent_change','Employees']
remove_symbols = ['$', '%',',','(',')','-']

def CleanColumns(df, cols):

    for col in cols: 
        if pd.api.types.is_object_dtype(df[col]):
            if type(df[col]) != type(float):
                for sym in remove_symbols: 
                    df[col] = df[col].str.replace(sym, "", regex = True)
                df[col] = df[col].str.strip()
                df[col] = df[col].astype('string')
                df[col] = df[col].fillna(0)
                try:
                    df[col] =pd.to_numeric(df[col], errors='coerce')
                    print("Converted " + col )
                except: 
                    print("Seems to be an issue with column " + col)
    return df 



#convert strings to floats
def convert(x):
    if 'M' in str(x):
        x = float(str(x).replace(',','').strip('$M '))/1000
    elif 'B' in str(x):
        x = float(str(x).replace(',','').strip('$B '))
    return x


for i in range(3,16):
    df_2022.iloc[:,i] = df_2022.iloc[:,i].apply(convert)
df_2022.head()





#build slider
selectie = st.slider(
    'slider',0,int(df_2022.size[0]),10)

#tijdelijke oplossing want 1,000 wilt niet converten naar int door kut komma (delete de laatste kolom met 1,000)
df_2022.drop(df_2022.tail(1).index,inplace=True)

#rank van string naar een nummer veranderen
df_2022[['Rank 2022']] = df_2022[['Rank 2022']].apply(pd.to_numeric)

bedrijven = df_2022[df_2022['Rank 2022'] <= selectie]

fig = make_subplots(rows=1, cols=2,
                   subplot_titles=("2021","2022",))
                   

fig.add_trace(
    go.Scatter(x=bedrijven['Assets 2021'], y=bedrijven['Profit 2021'],
        mode="markers+text",
        text=bedrijven["Name"],
        textposition="bottom center"
              
              ),
    row=1, col=1
)

fig.add_trace(
    go.Scatter( x=bedrijven['Assets 2022'], y=bedrijven['Profits 2022'],
        mode="markers+text",
        text=bedrijven["Name"],
        textposition="bottom center"
              ),
    row=1, col=2
)
fig.update_xaxes(title_text="Assets", row=1, col=1)
fig.update_xaxes(title_text="Assets", row=1, col=2)

fig.update_yaxes(title_text="Profit", row=1, col=1)
fig.update_yaxes(title_text="Profit",  row=1, col=2)

fig.update_layout(height=600, width=1000, title_text="Side By Side 2021 & 2022")


st.plotly_chart(fig)





