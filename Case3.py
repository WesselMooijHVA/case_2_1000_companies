#!/usr/bin/env python
# coding: utf-8

#importing required libraries and packages
import streamlit as st
import requests
import pandas as pd
import numpy as np
import json
import os
import authentication

from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
authentication.auth1(api)

#importing datasets from API
api.dataset_download_files('surajjha101/fortune-top-1000-companies-by-revenue-2022', unzip=True)
df_2022 = pd.read_csv('Fortune 1000 Companies by Revenue.csv')
api.dataset_download_files('shivamb/fortune-global-2000-companies-till-2021', unzip=True)
df_2021 = pd.read_csv('fortune_2000_in_2021.csv')

#changing column names to usable names
df_2021 = df_2021.rename(columns={'Rank':'Rank 2021', 'Sales':'Sales 2021', 'Profit':'Profit 2021', 'Assets':'Assets 2021', 'Market Value':'Market Value 2021'})
df_2022 = df_2022.rename(columns={'rank ':'Rank 2022', 'name ':'Name', 'revenues ':'Revenues 2022', 'profits ':'Profits 2022', 'assets':'Assets 2022', 'market_value ':'Market Value 2022', 'employees ':'Employees'})

#joining the tables into one dataframe
df_2022 = df_2022.join(df_2021.set_index('Name'), on='Name')
df_2022 = df_2022.dropna()

#printing the dataframe into streamlit
st.dataframe(df_2022)

