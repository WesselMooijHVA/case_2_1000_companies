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


# In[17]:


from case_2_1000_companies import authentication


api = KaggleApi()

authentication.auth_json(api)


# In[4]:


api.dataset_download_files('surajjha101/fortune-top-1000-companies-by-revenue-2022', unzip=True)
df_2022 = pd.read_csv('Fortune 1000 Companies by Revenue.csv')


# In[5]:


api.dataset_download_files('shivamb/fortune-global-2000-companies-till-2021', unzip=True)
df_2021 = pd.read_csv('fortune_2000_in_2021.csv')


# In[6]:


df_2021 = df_2021.rename(columns={'Rank':'Rank 2021', 'Sales':'Sales 2021', 'Profit':'Profit 2021', 'Assets':'Assets 2021', 'Market Value':'Market Value 2021'})


# In[7]:


df_2022 = df_2022.rename(columns={'rank ':'Rank 2022', 'name ':'Name', 'revenues ':'Revenues 2022', 'profits ':'Profits 2022', 'assets':'Assets 2022', 'market_value ':'Market Value 2022', 'employees ':'Employees'})


# In[8]:


df_2022 = df_2022.join(df_2021.set_index('Name'), on='Name')


# In[9]:


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





# In[10]:


def convert(x):
    if 'M' in str(x):
        x = float(str(x).replace(',','').strip('$M '))/1000
    elif 'B' in str(x):
        x = float(str(x).replace(',','').strip('$B '))
    return x


# In[11]:


for i in range(3,16):
    df_2022.iloc[:,i] = df_2022.iloc[:,i].apply(convert)


# In[12]:


df_2022['Market_Value_change']= df_2022['Market Value 2022'] - df_2022['Market Value 2021']


# In[13]:


corr = df_2022.corr()
ax, fig= plt.subplots(figsize=(20, 20))
sns.heatmap(corr, cmap="Greens", annot=True, vmin= -1, vmax= 1)


# In[19]:


df_2022['profit_per_employee_2021']= df_2022['Profit 2021']/ df_2022['Employees'] 
df_2022['profit_per_employee_2022']= df_2022['Profits 2022']/ df_2022['Employees']
df_2022['revenue_per_employee_2022']= df_2022['Revenues 2022']/ df_2022['Employees']
df_2022.fillna(0, axis= 1)


# In[20]:


df_2022_top100= df_2022[0:86]
df_2022_top100


# In[18]:


df_2022['profit_per_sale_2021']= df_2022['Profit 2021']/df_2022['Sales 2021']


# In[ ]:




