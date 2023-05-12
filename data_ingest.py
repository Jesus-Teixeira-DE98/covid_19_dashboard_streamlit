#==================================================#
#                     Imports                      #
#==================================================#

import requests
import pandas as pd
import inflection
import os
import dotenv
from sqlalchemy import create_engine

#==================================================#
#                     Variáveis                    #
#==================================================#

dotenv.load_dotenv(dotenv.find_dotenv()) 
url = "https://api.covid19api.com/summary"
username = os.getenv('username')
password =  os.getenv('password')
host = os.getenv('host')
port =  os.getenv('port')
database =  os.getenv('database')
con = f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}'

engine = create_engine(con)

#==================================================#
#                     Funções                     #
#==================================================#

def get_data(url):
    r = requests.get(url)
    data_raw = r.json()
    data = pd.DataFrame(data_raw['Countries'])
    return data

def transform(data):
    data.drop(columns=['Premium','NewRecovered', 'TotalRecovered', 'Date', 'ID', 'Country'], inplace = True)
    data.rename(columns={'Slug': 'Countries'}, inplace=True)
    cols_old = list(data.columns)
    cols_new = list(map(inflection.underscore, cols_old))
    data.columns = cols_new
    return data

def load(data):
    try:
        data.to_sql('covid_19', engine, if_exists = 'replace', method ='multi')
    except Exception as e:
        return print('Error: {}'.format(e))
    return None

#==================================================#
#                     Execução                     #
#==================================================#

if __name__ == '__main__':
    data = get_data(url)
    data = transform(data)
    data = load(data)