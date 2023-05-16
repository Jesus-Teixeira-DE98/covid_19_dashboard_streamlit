#==================================================#
#                     Imports                      #
#==================================================#
from sqlalchemy import create_engine
import pycountry
import pandas as pd
import streamlit as st
import plotly.io as pio
import plotly.express as px
import dotenv
import os

#==================================================#
#                     Functions                    #
#==================================================#

def extract():
    ''' 
    Extract data from database
    '''
    dotenv.load_dotenv(dotenv.find_dotenv()) 
    username = os.getenv('username')
    password =  os.getenv('password')
    host = os.getenv('host')
    port =  os.getenv('port')
    database =  os.getenv('database')
    con = f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}'
    engine = create_engine(con)
    data = pd.read_sql( 'select * from covid_19', engine)
    return data

def transform(data):
    '''
    cria e limpa colunas, extraí dados do pycountry e cria um dataframe com dados da iso-country.

    data: tipo dataframe, retorno da função extract.
    '''
    data['fatality_rate'] = data['total_deaths']/data['total_confirmed'] * 100 ## calculatting 
    data['countries']     = data['countries'].apply(lambda x: x.replace('-', ' '))
    # getting iso countries
    country_dict = {country.alpha_3: country.name.lower() for country in pycountry.countries}
    df = pd.DataFrame.from_dict(country_dict, orient='index', columns=['country_name'])
    df = df.reset_index()
    ## dataframe to create map 
    df2 = data.merge(df, left_on='countries', right_on='country_name', how='left')
    df2.drop(['index_x', 'country_name'], axis=1, inplace=True)
    return data, df2

def transform(data):
    data['fatality_rate'] = data['total_deaths']/data['total_confirmed'] * 100 ## calculatting 
    data['countries']     = data['countries'].apply(lambda x: x.replace('-', ' '))
    # getting iso countries
    country_dict = {country.alpha_3: country.name.lower() for country in pycountry.countries}
    df = pd.DataFrame.from_dict(country_dict, orient='index', columns=['country_name'])
    df = df.reset_index()
    ## dataframe to create map 
    df2 = data.merge(df, left_on='countries', right_on='country_name', how='left')
    df2.drop(['index_x', 'country_name'], axis=1, inplace=True)
    return data, df2

#==================================================#
#                     Get Data                     #
#==================================================#

data = extract()

#==================================================#
#                     Transform                    #
#==================================================#

data, df2 = transform(data)

#==================================================#
#                     Dashboard                    #
#==================================================#

## Cards ##
# Total Cases
total_cases = data['total_confirmed'].sum()
# Total Deaths
total_death = data['total_deaths'].sum()
# global fatality rate
global_fatality_rate = (total_death/total_cases) - 1
# Avg per country  
avg_fatality_rate = data['fatality_rate'].mean()

# top 10 covid_cases 
new_colors = ['#d0312d']
ax1 = data[['countries', 'total_confirmed']].sort_values(by=['total_confirmed'], ascending=False).reset_index(drop=True)
ax1 = ax1.loc[:9]
fig = px.bar(ax1, x='countries' ,y='total_confirmed', title="Countries with the most cases of covid", 
            text_auto=True, labels={'total_confirmed' : 'total cases confirmed'}, color_discrete_sequence=new_colors)
fig.update_traces(texttemplate='%{y:.2s}', textposition='outside', 
                  textfont=dict(size=14, family='Arial', color='black'))
fig.update_xaxes(title_font=dict(size=16, family='Arial', color='black'))
fig.update_yaxes(title_font=dict(size=16, family='Arial', color='black'))


# top 10 total deaths
ax2 = data[['countries', 'total_deaths']].sort_values(by=['total_deaths'], ascending=False).reset_index(drop=True)
ax2 = ax2.loc[:9]
fig2 = px.bar(ax2, x='countries' ,y='total_deaths', title="Countries with the most cases of covid", 
            text_auto=True, labels={'total_deaths' : 'total deaths'}, color_discrete_sequence=new_colors)
fig2.update_traces(texttemplate='%{y:.2s}', textposition='outside', 
                  textfont=dict(size=14, family='Arial', color='black'))
fig2.update_xaxes(title_font=dict(size=16, family='Arial', color='black'))
fig2.update_yaxes(title_font=dict(size=16, family='Arial', color='black'))


# top 10 fatality rate
ax3 = data[['countries', 'fatality_rate']].sort_values(by=['fatality_rate'], ascending=False).reset_index(drop=True)
ax3 = ax3.loc[:9]
fig3 = px.bar(ax3, x='countries' ,y='fatality_rate', title="Countries with the most cases of covid", 
            text_auto=True, labels={'fatality_rate' : 'fatality rate'}, color_discrete_sequence=new_colors)
fig3.update_traces(texttemplate='%{y:.2s}', textposition='outside', 
                  textfont=dict(size=14, family='Arial', color='black'))
fig3.update_xaxes(title_font=dict(size=16, family='Arial', color='black'))
fig3.update_yaxes(title_font=dict(size=16, family='Arial', color='black'))


# top 10 new confirmed 
ax4 = data[['countries', 'new_confirmed']].sort_values(by=['new_confirmed'], ascending=False).reset_index(drop=True)
ax4 = ax4.loc[:9]
fig4 = px.bar(ax4, x='countries' ,y='new_confirmed', title="Countries with the most cases of covid", 
            text_auto=True, labels={'new_confirmed' : 'new confirmed'}, color_discrete_sequence=new_colors)
fig4.update_traces(texttemplate='%{y:.2s}', textposition='outside', 
                  textfont=dict(size=14, family='Arial', color='black'))
fig4.update_xaxes(title_font=dict(size=16, family='Arial', color='black'))
fig4.update_yaxes(title_font=dict(size=16, family='Arial', color='black'))


# Worldmap 
fig5 = px.scatter_geo(df2, locations="index_y", size="total_confirmed", hover_name="countries",
                     projection="natural earth", color_continuous_scale="icefire")


st.title('Covid 19 - World Data')

