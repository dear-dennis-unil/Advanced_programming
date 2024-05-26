# 0.0 Importing modules
import numpy as np
import pandas as pd
from dataprep.clean import clean_headers
from datetime import date, datetime
import plotly.express as px
import geopandas as gpd # To import shp type files
from ridgeplot import ridgeplot # For the ridgeplot
from ridgeplot.datasets import load_probly
import plotly.graph_objects as go
import re

# 0.1 Functions for formatting tables
def add_commas(x):
    return '{:,.0f}'.format(x)

def four_digits(x):
    return '{:,.4f}'.format(x)




# 1. Importing NYC collisions data

# 1. 1 Working space path

# 1.2 Importing data and assigning to nyc_collisions DataFrame
nyc_collisions = pd.read_csv("inputs/data/nyc_car_collisions.csv")

nyc_collisions_original = nyc_collisions.head(200)
# 1.3 Cleaning names and converting columns.
nyc_collisions = (
  nyc_collisions
  .pipe(clean_headers, case = 'snake') #cleans_names
  .assign(
      accident_date = lambda x: pd.to_datetime(x['crash_date'], format ='%m/%d/%Y'), 
      accident_time = lambda x: pd.to_datetime(x['crash_time'], format = '%H:%M')
      )
)

# 1.4 Creating the nyc_collisions_id DataFrame.
nyc_collisions_id = ( 
    nyc_collisions
    .assign(
        accident_year  = lambda x: x['accident_date'].dt.year,
        accident_month = lambda x: x['accident_date'].dt.month, 
        accident_day   = lambda x: x['accident_date'].dt.day 
        )
)

nyc_collisions_id_head = nyc_collisions_id.head(200)

# 1.4.1 Columns to select from the nyc_collisions_id DataFrame.
columns_to_select = (
    ['collision_id', 
     'latitude',
     'longitude', 
     'accident_date',
     'accident_year',
     'accident_month',
     'accident_day',
     'accident_time'] +
    nyc_collisions_id
    .columns[pd.Series(nyc_collisions_id.columns)
             .str.contains('number_of')]
    .to_list()
)

# 1.4.2 Calculating total number of victims.
nyc_collisions_id = ( 
    nyc_collisions_id
    .get(columns_to_select)
    .assign(victims = lambda x: x['number_of_persons_injured'] + x['number_of_persons_killed']) 
    
    )

# 1.5 Missing variable summary
nyc_collisions_id_missing = (
    pd.DataFrame({
        'variable': nyc_collisions_id.columns,
        'missing_values_n': nyc_collisions_id.isnull().sum(),
        'missing_values_percentage': nyc_collisions_id.isnull().mean() *100}) 
    .assign(non_missing_values_n =  lambda x: len(nyc_collisions) - x['missing_values_n'])
    .reset_index(drop=True)
    .sort_values('missing_values_percentage', ascending = False) 
    .get(['variable', 'non_missing_values_n', 'missing_values_n', 'missing_values_percentage'])
        )




# 1.6 Missing variable summary filtered
nyc_collisions_id_missing_filtered = (
    nyc_collisions_id_missing
    .query('missing_values_percentage > 0')
        )



# 1.6.2 Plot
nyc_collisions_id_missing_filtered_lollipop_plot = (
    px.bar(nyc_collisions_id_missing_filtered, 
            x = 'missing_values_percentage',
            y ='variable', 
            labels = {'missing_values_percentage' : 'Percentage %', 
                      'variable' : 'Variable' }, 
            template = 'none'
    )
)

fig_lollipop = (
    px.scatter(nyc_collisions_id_missing_filtered,
            x = 'missing_values_percentage',
            y ='variable', 
            title='Lollipop Chart', 
            template = 'none'
    )
    .update_traces(
        marker=dict(color = 'green', size = 10)
    )
    .add_traces(
        px.bar(nyc_collisions_id_missing_filtered,
            x = 'missing_values_percentage',
            y = 'variable'
        )
        .update_traces(width = 0.010, marker=dict(color = 'gray'))
        .data[0]
    )
    .update_yaxes(autorange='reversed')
)



#nyc_collisions_id_missing_filtered_lollipop_plot.show()
# 2 nyc_yearly_statistics
nyc_collisions_yearly_statistics = (
    nyc_collisions_id
    .groupby('accident_year')
    .agg(
        collisions_n=('collision_id', 'count'),
        victims=('victims', 'sum'),
        deaths=('number_of_persons_killed', 'sum'),
        injuries=('number_of_persons_injured', 'sum')
    )
    .reset_index()
    .assign(
        rate_victims=lambda x: x['victims'] / x['collisions_n'],
        rate_deaths=lambda x: x['deaths'] / x['collisions_n'],
        rate_injuries=lambda x: x['injuries'] / x['collisions_n']
    )
)

# This was done to avoid a max recursion overreach error in Shiny.
# As the code 
# schema_df = nyc_collisions.dtypes.reset_index()
# schema_df.columns = ['Column', 'DataType']
# Did NOT work

schema_df = (
    pd.DataFrame(
        [['CRASH DATE', 'object'],
        ['CRASH TIME', 'object'],
        ['BOROUGH','object'],
        ['ZIP CODE', ',object'],
        ['LATITUDE', 'float64'],
        ['LONGITUDE', 'float64'],
        ['LOCATION', 'object'],
        ['ON STREET NAME', 'object'],
        ['CROSS STREET NAME', 'object'],
        ['OFF STREET NAME', 'object'],
        ['NUMBER OF PERSONS INJURED', 'float64'],
        ['NUMBER OF PERSONS KILLED', 'float64'],
        ['NUMBER OF PEDESTRIANS INJURED', 'int64'],
        ['NUMBER OF PEDESTRIANS KILLED', 'int64'],
        ['NUMBER OF CYCLIST INJURED', 'int64'],
        ['NUMBER OF CYCLIST KILLED', 'int64'],
        ['NUMBER OF MOTORIST INJURED', 'int64'],
        ['NUMBER OF MOTORIST KILLED', 'int64'],
        ['CONTRIBUTING FACTOR VEHICLE 1', 'object'],
        ['CONTRIBUTING FACTOR VEHICLE 2', 'object'],
        ['CONTRIBUTING FACTOR VEHICLE 3', 'object'],
        ['CONTRIBUTING FACTOR VEHICLE 4', 'object'],
        ['CONTRIBUTING FACTOR VEHICLE 5', 'object'],
        ['COLLISION_ID', 'int64'],
        ['VEHICLE TYPE CODE 1', 'object'],
        ['VEHICLE TYPE CODE 2', 'object'],
        ['VEHICLE TYPE CODE 3', 'object'],
        ['VEHICLE TYPE CODE 4', 'object'],
        ['VEHICLE TYPE CODE 5', 'object']],
        columns= [ 'Column', 'Class']
    )
 )


clean_schema_df = (
    pd.DataFrame([
        ['crash_date', 'character', 1],
        ['crash_time', 'double', 1],
        ['borough', 'character', 1],
        ['zip_code', 'double', 1],
        ['latitude', 'double', 1],
        ['longitude', 'double', 1],
        ['location', 'character', 1],
        ['collision_id', 'double', 1],
        ['accident_date', 'double', 1],
        ['accident_time', 'double', 1],
        ['street_name_category', 'double', 3],
        ['number_of_category', 'double', 8],
        ['contributing_factor_category', 'double', 5],
        ['vehicle_type_category', 'double', 5]], 
        columns = ['Variable', 'Variable type', 'Number of columns per variable']
    )
)


# Format table of missing values
nyc_collisions_id_missing_filtered[['non_missing_values_n', 'missing_values_n']] = (
    nyc_collisions_id_missing_filtered
    .filter(['non_missing_values_n', 'missing_values_n'])
    .applymap(lambda x: add_commas(x)) 
    )


nyc_collisions_id_missing_filtered['missing_values_percentage'] = (
    nyc_collisions_id_missing_filtered['missing_values_percentage']
    .map(lambda x: four_digits(x)) 
    )



