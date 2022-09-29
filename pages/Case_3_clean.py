#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip install kaggle
#!pip install streamlit


# In[14]:


import requests
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import authentication

api = KaggleApi()

authentication.auth_json(api)


# In[ ]:





# In[15]:


api.dataset_download_files('surajjha101/fortune-top-1000-companies-by-revenue-2022', unzip=True)
df_2022 = pd.read_csv('Fortune 1000 Companies by Revenue.csv')


# In[16]:


api.dataset_download_files('shivamb/fortune-global-2000-companies-till-2021', unzip=True)
df_2021 = pd.read_csv('fortune_2000_in_2021.csv')


# In[17]:


df_2021 = df_2021.rename(columns={'Rank':'Rank 2021', 'Sales':'Sales 2021', 'Profit':'Profit 2021', 'Assets':'Assets 2021', 'Market Value':'Market Value 2021'})
df_2021


# In[18]:


df_2022 = df_2022.rename(columns={'rank ':'Rank 2022', 'name ':'Name', 'revenues ':'Revenues 2022', 'profits ':'Profits 2022', 'assets':'Assets 2022', 'market_value ':'Market Value 2022', 'employees ':'Employees'})
df_2022


# In[19]:


df_2022 = df_2022.join(df_2021.set_index('Name'), on='Name')
df_2022


# In[20]:


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


# In[21]:


rev


# In[22]:


def convert(x):
    if 'M' in str(x):
        x = float(str(x).replace(',','').strip('$M '))/1000
    elif 'B' in str(x):
        x = float(str(x).replace(',','').strip('$B '))
    return x


# In[23]:


for i in range(3,16):
    df_2022.iloc[:,i] = df_2022.iloc[:,i].apply(convert)
df_2022.head()


# In[24]:


fig = px.scatter(df_2022, x='Market Value 2021', y= 'Market Value 2022', color = 'Name')
st.plotly_chart(fig)
fig.show()


# In[ ]:





# In[26]:


fig = px.histogram(df_2022, y='Employees', color = 'Name')
fig.show()


# In[27]:


fig = px.scatter(df_2022, x='Assets 2022', y= 'Profits 2022', color = 'Name', marginal_x="histogram", marginal_y="rug")
fig.update_yaxes(categoryorder='category ascending')
st.plotly_chart(fig)
fig.show()


# In[28]:


fig = px.scatter(df_2022, x='Assets 2021', y= 'Profit 2021', color = 'Name', marginal_x="histogram", marginal_y="rug")
fig.update_yaxes(categoryorder='category ascending')
st.plotly_chart(fig)
fig.show()


# In[32]:


fig = px.scatter(df_2022, x='Assets 2021', y= 'Assets 2022', color = 'Name', marginal_x="histogram", marginal_y="rug")
fig.update_yaxes(categoryorder='category ascending')
st.plotly_chart(fig)
fig.show()


# In[ ]:




