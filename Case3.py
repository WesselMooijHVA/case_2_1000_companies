#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip install 
#!pip install streamlit


# In[2]:


import streamlit as st
import requests
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import numpy as np
import json
import os


# In[3]:


api = KaggleApi()
#doesnt work in streamlit???
#with open('kaggle.json') as json_file:
#    config_data = json.load(json_file)
os.environ['KAGGLE_USERNAME'] = 'davevanderschouw'
os.environ['KAGGLE_KEY'] = 'dea650c8a5aa2e60e1af506563daf342'


# In[4]:


api.authenticate()


# In[5]:


api.dataset_download_files('surajjha101/fortune-top-1000-companies-by-revenue-2022', unzip=True)
df_2022 = pd.read_csv('Fortune 1000 Companies by Revenue.csv')


# In[6]:


api.dataset_download_files('shivamb/fortune-global-2000-companies-till-2021', unzip=True)
df_2021 = pd.read_csv('fortune_2000_in_2021.csv')


# In[7]:


df_2021 = df_2021.rename(columns={'Rank':'Rank 2021', 'Sales':'Sales 2021', 'Profit':'Profit 2021', 'Assets':'Assets 2021', 'Market Value':'Market Value 2021'})
df_2021


# In[8]:


df_2022 = df_2022.rename(columns={'rank ':'Rank 2022', 'name ':'Name', 'revenues ':'Revenues 2022', 'profits ':'Profits 2022', 'assets':'Assets 2022', 'market_value ':'Market Value 2022', 'employees ':'Employees'})
df_2022


# In[9]:


df_2022 = df_2022.join(df_2021.set_index('Name'), on='Name')
df_2022


# In[10]:


df_2022.isna().sum()


# In[11]:


df_2022 = df_2022.dropna()
df_2022['Country'].value_counts()


# In[12]:


st.dataframe(df_2022)

