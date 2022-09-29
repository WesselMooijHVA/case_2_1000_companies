#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip install kaggle


# In[2]:


import requests
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st


# In[3]:


import authentication


api = KaggleApi()

authentication.auth_json(api)


# In[4]:


st.title('dataframe hervorming en Market Value')


# In[5]:


api.dataset_download_files('surajjha101/fortune-top-1000-companies-by-revenue-2022', unzip=True)
df_2022 = pd.read_csv('Fortune 1000 Companies by Revenue.csv')


# In[6]:


api.dataset_download_files('shivamb/fortune-global-2000-companies-till-2021', unzip=True)
df_2021 = pd.read_csv('fortune_2000_in_2021.csv')


# In[7]:


df_2021 = df_2021.rename(columns={'Rank':'Rank 2021', 'Sales':'Sales 2021', 'Profit':'Profit 2021', 'Assets':'Assets 2021', 'Market Value':'Market Value 2021'})


# In[8]:


df_2022 = df_2022.rename(columns={'rank ':'Rank 2022', 'name ':'Name', 'revenues ':'Revenues 2022', 'profits ':'Profits 2022', 'assets':'Assets 2022', 'market_value ':'Market Value 2022', 'employees ':'Employees'})


# In[9]:


df_2022 = df_2022.join(df_2021.set_index('Name'), on='Name')


# In[10]:


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


# In[ ]:





# In[11]:


def convert(x):
    if 'M' in str(x):
        x = float(str(x).replace(',','').strip('$M '))/1000
    elif 'B' in str(x):
        x = float(str(x).replace(',','').strip('$B '))
    return x


# In[12]:


for i in range(3,16):
    df_2022.iloc[:,i] = df_2022.iloc[:,i].apply(convert)


# In[13]:


df_2022['Market_Value_change']= df_2022['Market Value 2022'] - df_2022['Market Value 2021']


# In[14]:


corr = df_2022.corr()
fig2= px.imshow(corr, text_auto= True, color_continuous_scale='RdBu_r', width= 1200 , height= 1000 )
fig2.update_layout(title='heatmap van de verschillende correlaties tussen de kolommen')
fig2.show()
st.plotly_chart(fig2)


# In[15]:


df_2022['profit_per_employee_2021']= df_2022['Profit 2021']/ df_2022['Employees'] 
df_2022['profit_per_employee_2022']= df_2022['Profits 2022']/ df_2022['Employees']
df_2022['revenue_per_employee_2022']= df_2022['Revenues 2022']/ df_2022['Employees']
df_2022.fillna(0, axis= 1)


# In[16]:


kolommen= df_2022.columns
st.sidebar.selectbox('selecteer de variabelen',('Rank 2022', 'Name', 'Revenues 2022', 'revenue_percent_change',
       'Profits 2022', 'profits_percent_change', 'Assets 2022',
       'Market Value 2022', 'change_in_rank', 'Employees', 'Rank 2021',
       'Country', 'Sales 2021', 'Profit 2021', 'Assets 2021',
       'Market Value 2021', 'Market_Value_change', 'profit_per_employee_2021',
       'profit_per_employee_2022', 'revenue_per_employee_2022',
       'profit_per_sale_2021'))
selectboxselection= df_2022 == kolommen
st.dataframe(selectboxselection)


# In[21]:


df_2022_top100= df_2022[0:86]
df_2022_top100


# In[18]:


df_2022['profit_per_sale_2021']= df_2022['Profit 2021']/df_2022['Sales 2021']


# In[19]:


fig= px.bar(df_2022_top100, x= 'Name', y= 'Market_Value_change', hover_data=['Market Value 2022', 'Market Value 2021'], color='Market_Value_change', height=600)
fig.update_layout(xaxis={'categoryorder':'total descending'})
fig.update_xaxes(title_text='Bedrijfsnaam')
fig.update_yaxes(title_text='Verandering in Marktwaarde')
fig.show()


# In[20]:


st.plotly_chart(fig)


# In[ ]:




