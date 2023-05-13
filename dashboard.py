from sqlalchemy import create_engine
import pandas as pd
import plotly.io as pio
import plotly.express as px
import dotenv
import os

dotenv.load_dotenv(dotenv.find_dotenv()) 

username = os.getenv('username')
password =  os.getenv('password')
host = os.getenv('host')
port =  os.getenv('port')
database =  os.getenv('database')
con = f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}'
engine = create_engine(con)

data = pd.read_sql( 'select * from covid_19', engine)

data['fatality_rate'] = data['total_deaths']/data['total_confirmed'] * 100 
# Identifing the proportion of deaths for each country

# Total Deaths
total_death = data['total_deaths'].sum()
# Avg 
avg_fatality_rate = data['fatality_rate'].mean()

# top 10 covid_cases 
ax1 = data[['countries', 'total_confirmed']].sort_values(by=['total_confirmed'], ascending=False).reset_index(drop=True)
ax1 = ax1.loc[:9]
pio.renderers.default = "notebook"
fig = px.bar(ax1, x='countries' ,y='total_confirmed')
fig.show(renderer='vscode')

# top 10 total deaths
ax2 = data[['countries', 'total_deaths']].sort_values(by=['total_deaths'], ascending=False).reset_index(drop=True)
ax2 = ax2.loc[:9]

# top 10 fatality rate
ax3 = data[['countries', 'fatality_rate']].sort_values(by=['fatality_rate'], ascending=False).reset_index(drop=True)
ax3 = ax3.loc[:9]

# top 10 new confirmed 
ax4 = data[['countries', 'new_confirmed']].sort_values(by=['new_confirmed'], ascending=False).reset_index(drop=True)
ax4 = ax4.loc[:9]
