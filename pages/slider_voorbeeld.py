import requests
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px


import authentication

api = KaggleApi()

authentication.auth_json(api)

api.dataset_download_files('surajjha101/fortune-top-1000-companies-by-revenue-2022', unzip=True)
df_2022 = pd.read_csv('Fortune 1000 Companies by Revenue.csv')

api.dataset_download_files('shivamb/fortune-global-2000-companies-till-2021', unzip=True)
df_2021 = pd.read_csv('fortune_2000_in_2021.csv')


df_2021 = df_2021.rename(columns={'Rank':'Rank 2021', 'Sales':'Sales 2021', 'Profit':'Profit 2021', 'Assets':'Assets 2021', 'Market Value':'Market Value 2021'})
df_2021
df_2022 = df_2022.rename(columns={'rank ':'Rank 2022', 'name ':'Name', 'revenues ':'Revenues 2022', 'profits ':'Profits 2022', 'assets':'Assets 2022', 'market_value ':'Market Value 2022', 'employees ':'Employees'})
df_2022

df_2022 = df_2022.join(df_2021.set_index('Name'), on='Name')
df_2022



#selectie maken van 0 tot maximum size van de dataframe
selectie = st.slider(
    'selectie text',0,int(df_2022.size),10)

#tijdelijke oplossing want 1,000 wilt niet converten naar int door kut komma (delete de laatste kolom met 1,000)
df_2022.drop(df_2022.tail(1).index,inplace=True)

#rank van string naar een nummer veranderen
df_2022[['Rank 2022']] = df_2022[['Rank 2022']].apply(pd.to_numeric)

#alleen bedrijven selecteren die in de selectie zijn
bedrijven = df_2022[df_2022['Rank 2022'] <= selectie]

#display plot in streamlit
fig = px.scatter(bedrijven, x = "Profit 2021", y = "Profits 2022", color = "Name")
st.plotly_chart(fig)
