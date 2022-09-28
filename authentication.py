def auth():
  #imports
  from kaggle.api.kaggle_api_extended import KaggleApi
  import json
  import os

  #initiating API and setting username and key as environment variables
  api = KaggleApi()
  with open('kaggle.json') as json_file:
    config_data = json.load(json_file)
  os.environ['KAGGLE_USERNAME'] = config_data['username']
  os.environ['KAGGLE_KEY'] = config_data['key']

  #authenticate using environment variables
  api.authenticate()  
