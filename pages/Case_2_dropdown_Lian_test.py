#!/usr/bin/env python
# coding: utf-8

# In[107]:


#!pip install kaggle


# In[108]:


import requests
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st


# In[109]:


import authentication

api = KaggleApi()

authentication.auth_json(api)


# In[110]:


st.title('dataframe verwerking en eerste analyses')


# In[111]:


api.dataset_download_files('surajjha101/fortune-top-1000-companies-by-revenue-2022', unzip=True)
df_2022 = pd.read_csv('Fortune 1000 Companies by Revenue.csv')


# In[112]:


api.dataset_download_files('shivamb/fortune-global-2000-companies-till-2021', unzip=True)
df_2021 = pd.read_csv('fortune_2000_in_2021.csv')


# In[113]:


df_2021 = df_2021.rename(columns={'Rank':'Rank 2021', 'Sales':'Sales 2021', 'Profit':'Profit 2021', 'Assets':'Assets 2021', 'Market Value':'Market Value 2021'})


# In[114]:


df_2022 = df_2022.rename(columns={'rank ':'Rank 2022', 'name ':'Name', 'revenues ':'Revenues 2022', 'profits ':'Profits 2022', 'assets':'Assets 2022', 'market_value ':'Market Value 2022', 'employees ':'Employees'})


# In[115]:


df_2022 = df_2022.join(df_2021.set_index('Name'), on='Name')


# In[116]:


st.subheader('2022 data bruikbaar maken voor berekeningen')
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

rev = CleanColumns(df_2022, col_convert)


# In[117]:


rev


# In[118]:


st.subheader('2021 data bruikbaar maken voor berekeningen')
def convert(x):
    if 'M' in str(x):
        x = float(str(x).replace(',','').strip('$M '))/1000
    elif 'B' in str(x):
        x = float(str(x).replace(',','').strip('$B '))
    return x
for i in range(3,16):
    df_2022.iloc[:,i] = df_2022.iloc[:,i].apply(convert)
df_2022.head()


# In[119]:


df_2022


# In[120]:


import plotly as plt
import plotly.graph_objects as go
import plotly.express as px

#top 5 bedrijven winst 2021-2022 dropdownmenu

#top_5_bedrijven aanmaken
top_5_bedrijven = df_2022.head()

#scatterplot aanmaken
fig = px.scatter(top_5_bedrijven, x = "Profit 2021", y = "Profits 2022", color = "Name")

#dropdownmenu aanmaken
dropdown_buttons = [{"label":"Walmart", "method":"update","args":[{"visible":[True, False, False, False, False]},{"title":"Walmart"}]}, {"label":"Amazon", "method":"update","args":[{"visible":[False, True, False, False, False]},{"title":"Amazon"}]},{"label":"Apple", "method":"update","args":[{"visible":[False,False,True, False, False]},{"title":"Apple"}]},{"label":"CVS Health", "method":"update","args":[{"visible":[True, False, False, False, False]},{"title":"CVS Health"}]},{"label":"UnitedHealth Group", "method":"update","args":[{"visible":[True, False, False, False, False]},{"title":"UnitedHealth Group"}]}]
#dropdownmenu toevoegen
fig.update_layout({"updatemenus":[{"type":"dropdown","x": 1.3,"y":0.5,"showactive":True,"active":0,"buttons": dropdown_buttons}]})
#titels/labels aanmaken
fig.update_layout(legend_title_text = "Namen bedrijven", title = "Scatterplot top 5 bedrijven winst 2021 vs winst 2022 ")
fig.update_xaxes(title_text="Winst 2021")
fig.update_yaxes(title_text="Winst 2022")

#figuur plotten in streamlit
st.plotly_chart(fig)
fig.show()


# In[125]:


#top 5 bedrijven winst 2021 2022 slider


#import plotly as plt
#import plotly.graph_objects as go
#import plotly.express as px

#fig = px.scatter(top_5_bedrijven, x = "Market Value 2022", y = "Market Value 2021", color = "Name")

#sliders = [{"steps":[{"method":"update","label":"Walmart","args":[{"visible":[True, False, False, False, False]}]}, {"method":"update","label":"Amazon","args":[{"visible":[False, True, False, False, False]}]}, {"method":"update","label":"Apple","args":[{"visible":[False, False, True, False, False]}]}, {"method":"update","label":"CVS Health","args":[{"visible":[False, False, False, True, False]}]}, {"method":"update","label":"UnitedHealth Group","args":[{"visible":[False, False, False, False, True]}]}]}]

#fig.update_layout({"sliders":sliders})

#st.plotly_chart(fig)

