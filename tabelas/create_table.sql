create table db_covid.public.covid_19 (
id SERIAL primary key,
country_code varchar(200),
countries varchar(200),
new_confirmed int,
total_confirmed int,
new_deaths int,
total_deaths int
)