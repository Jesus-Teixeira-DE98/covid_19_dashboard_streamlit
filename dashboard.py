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






## ================================================ 
### Geral                                            
### ================================================ 
st.set_page_config(layout='wide')
st.header('Covid 19 - World Data') #Escrever cabeçalho 
### ================================================ 
### Side Bar                                      
### ================================================ 

st.sidebar.markdown("# Explore data")
st.sidebar.markdown("""---""")
st.sidebar.title("Filters")

### Filters ###
min_slider = int(data['fatality_rate'].min())
max_slider = int(data['fatality_rate'].max()) 
slider_select = st.sidebar.slider('Fatality Rate(%)', min_value=min_slider, max_value=max_slider, value=max_slider )
lines_filter1 = data['fatality_rate'] <= slider_select
data_raw = data.loc[lines_filter1, :]
select = list(data_raw['countries'].unique())
countries_selected = st.sidebar.multiselect('Chose a Contry', select, default=None)
lines_filter2 = data['countries'].isin(countries_selected)
data_raw1 = data_raw.loc[lines_filter1, :]

### main page ###

tab1, tab2 = st.tabs(['Project Description', 'Graphs and Data'])

with tab1:
    st.title('Project Details')
    ## Describe all the project 
    ## Source of information 
    ## GIT HUB link 
    ## Linkedin

with tab2:
    st.title('Global Metrics')
    ## Cards ##
    # Total Cases
    total_cases = data_raw1['total_confirmed'].sum()
    # Total Deaths
    total_death = data_raw1['total_deaths'].sum()
    # global fatality rate
    global_fatality_rate = round((total_death/total_cases), 2)
    # Avg per country  
    avg_fatality_rate = round(data_raw1['fatality_rate'].mean(), 2)
    st.markdown("""---""")
    st.header('Total Cases, Deaths and Rate')
    st.subheader('Algumas métricas importantes apresentadas como cartão')
    col1, col2, col3, col4, = st.columns(4)
    with col1:
        st.metric(label="Total Cases", value=total_cases )
    with col2:
        st.metric(label="Total Deaths", value=total_death )
    with col3:
        st.metric(label="Global Fatality Rate", value=global_fatality_rate )
    with col4:
        st.metric(label="Avarage Fatality Rate", value=avg_fatality_rate )

    st.markdown("""---""")
    st.header('Top 10 Countries')
    # top 10 covid_cases 
    new_colors = ['#d0312d']
    ax1 = data[['countries', 'total_confirmed']].sort_values(by=['total_confirmed'], ascending=False).reset_index(drop=True)
    ax1 = ax1.loc[:9]
    fig = px.bar(ax1, x='countries' ,y='total_confirmed', title="Countries with the most cases of covid", 
                text_auto=True, labels={'total_confirmed' : 'total cases confirmed'}, color_discrete_sequence=new_colors)
    fig.update_traces(texttemplate='%{y:.2s}', textposition='outside', 
                    textfont=dict(size=14, family='Arial', color='white'))
    fig.update_xaxes(title_font=dict(size=16, family='Arial', color='white'))
    fig.update_yaxes(title_font=dict(size=16, family='Arial', color='white'))


    # top 10 total deaths
    ax2 = data[['countries', 'total_deaths']].sort_values(by=['total_deaths'], ascending=False).reset_index(drop=True)
    ax2 = ax2.loc[:9]
    fig2 = px.bar(ax2, x='countries' ,y='total_deaths', title="Countries with the most cases of covid", 
                text_auto=True, labels={'total_deaths' : 'total deaths'}, color_discrete_sequence=new_colors)
    fig2.update_traces(texttemplate='%{y:.2s}', textposition='outside', 
                    textfont=dict(size=14, family='Arial', color='white'))
    fig2.update_xaxes(title_font=dict(size=16, family='Arial', color='white'))
    fig2.update_yaxes(title_font=dict(size=16, family='Arial', color='white'))


    # top 10 fatality rate
    ax3 = data[['countries', 'fatality_rate']].sort_values(by=['fatality_rate'], ascending=False).reset_index(drop=True)
    ax3 = ax3.loc[:9]
    fig3 = px.bar(ax3, x='countries' ,y='fatality_rate', title="Countries with the most cases of covid", 
                text_auto=True, labels={'fatality_rate' : 'fatality rate'}, color_discrete_sequence=new_colors)
    fig3.update_traces(texttemplate='%{y:.2s}', textposition='outside', 
                    textfont=dict(size=14, family='Arial', color='white'))
    fig3.update_xaxes(title_font=dict(size=16, family='Arial', color='white'))
    fig3.update_yaxes(title_font=dict(size=16, family='Arial', color='white'))


    # top 10 new confirmed 
    ax4 = data[['countries', 'new_confirmed']].sort_values(by=['new_confirmed'], ascending=False).reset_index(drop=True)
    ax4 = ax4.loc[:9]
    fig4 = px.bar(ax4, x='countries' ,y='new_confirmed', title="Countries with the most cases of covid", 
                text_auto=True, labels={'new_confirmed' : 'new confirmed'}, color_discrete_sequence=new_colors)
    fig4.update_traces(texttemplate='%{y:.2s}', textposition='outside', 
                    textfont=dict(size=14, family='Arial', color='white'))
    fig4.update_xaxes(title_font=dict(size=16, family='Arial', color='white'))
    fig4.update_yaxes(title_font=dict(size=16, family='Arial', color='white'))

    col5, col6 = st.columns(2)
    with col5:
        st.plotly_chart(fig, use_container_width=True)
        st.plotly_chart(fig2, use_container_width=True)
    with col6: 
        st.plotly_chart(fig3, use_container_width=True)
        st.plotly_chart(fig4, use_container_width=True)    

    st.markdown("""---""") 
    st.header('Covid World Map')      
    # Worldmap 
    fig5 = px.scatter_geo(df2, locations="index_y", size="total_confirmed", hover_name="countries",
                     projection="natural earth", color_continuous_scale="icefire")
    st.plotly_chart(fig5, use_container_width=True) 

