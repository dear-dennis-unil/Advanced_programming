# 0.0 Importing libraries
import numpy as np
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import n_colors
import scripts.ps_01_data_cleansing_and_tidying as ps01
import scripts.ps_02_exploratory_data_analysis as ps02


# 0.1 Functions for formatting tables
def add_commas(x):
    return '{:,.0f}'.format(x)

def four_digits(x):
    return '{:,.4f}'.format(x)


# 0.2 Importing data
agg_data = (
    gpd.read_file("inputs/data/aggregated_neighbourhood_data/agg_data.shp")
    .dropna(subset=['accdnt_'])  # Filter rows where accdnt_ is not NA
)

# 1.0 Where?
# 1.1 Map ---> In it's own python script. The relative path is './scripts/ps_03_map.py'

# 1.2 Calculating top 3 victims for a
top_3_victims = (
    agg_data
    .groupby(['accdnt_', 'ntaname'])
    .agg(victims=('victims', 'sum')) 
    .reset_index()
    .groupby('accdnt_')
    .apply(lambda x: x.nlargest(3, 'victims'))
    .reset_index(drop = True)
    )


# 2.0 When?
# 2.1 Facet grids
fig_facet = (
    px.line(ps02.nyc_collisions_month_statistics, 
            x = 'accident_month', 
            y = 'victims',
            color = 'accident_year',
            facet_col = 'accident_year', 
            facet_col_wrap = 4,
            line_shape = 'linear',
            title = 'Collision victims from 2012 to 2023', 
            template = 'none')
    .update_layout(showlegend = False, height = 600, width = 1000)
    .update_yaxes(range = [2000, 6000])

)

# 2.2 Boxplots
# Data 
day_of_week_df = pd.DataFrame({'day_of_the_week' : ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                               'accident_weekday': list(np.arange(0, 7))})

nyc_collisions_wday_hour = (
    ps01.nyc_collisions_id
    .assign(accident_weekday = lambda x: x['accident_date'].dt.dayofweek,
            accident_hour = lambda x: x['accident_time'].dt.hour)
    .groupby(['accident_weekday', 'accident_hour']) 
    .agg(collision_n=('collision_id', 'count'),
         victims_n=('victims', 'sum'))
    .reset_index()
    .merge(day_of_week_df, on = 'accident_weekday', how = 'left')
)


# BoxPlot
fig_boxplot = (
    px.box(nyc_collisions_wday_hour,
             x = 'day_of_the_week',
             y = 'collision_n', 
             color = 'day_of_the_week',
             title = "Number of car collisions considerably consistent from Monday to Friday",
             labels = {'day_of_the_week': 'Day of the week', 'collision_n': 'Number of car collisions'},
             template = 'none'
    )
)


# 2.4 Violin plots

# Data
nyc_collisions_wday_hour_ungrouped = (
    ps01.nyc_collisions_id
    .assign(accident_weekday = lambda x: x['accident_date'].dt.dayofweek,
            accident_hour = lambda x: x['accident_time'].dt.hour)
    .get(['accident_weekday', 'accident_hour' ])
    .sort_values(by=['accident_weekday', 'accident_hour'])
    .merge(day_of_week_df, on = 'accident_weekday', how = 'left')
)

# ViolinPlot
fig_violin_plots = (
    px.violin(nyc_collisions_wday_hour_ungrouped,
           x = 'day_of_the_week',
           y = 'accident_hour',
           color = 'day_of_the_week', 
           title = "Number of car collisions per hour of the day", 
           labels = {'day_of_the_week': 'Day of the week', 'accident_hour': 'Hour of the accidenr'}, 
           template = 'none')
    .update_traces(side='positive', width = 1.5, points=False)
    .update_layout(showlegend = False)
    .update_yaxes(tickvals=list(range(24)))
           
)


# 3.0 Why?
nyc_collisions_why = (
    ps01.nyc_collisions
    .filter(like='contributing_factor')
    .melt(var_name='contributing_factor_number', value_name='contributing_factor')
    .dropna(subset=['contributing_factor'])
    .groupby('contributing_factor')
    .size()
    .reset_index(name='n')
    .sort_values(by='n', ascending=False)
    .head(11)
    .query('contributing_factor != "Unspecified"')
)


# Formating table for shiny app

nyc_collisions_why['n'] = (
    nyc_collisions_why['n']
    .map(lambda x: add_commas(x)) 
    )


# 4.0 How many?

nyc_collisions_yearly_statistics = (
    ps01.nyc_collisions_id
    .groupby('accident_year')
    .agg(
        collisions_n=('accident_year', 'size'),
        victims=('victims', 'sum'),
        deaths=('number_of_persons_killed', 'sum'),
        injuries=('number_of_persons_injured', 'sum'),
        months_n=('accident_month', lambda x: x.max() - x.min() + 1)
    )
    .reset_index()
)

nyc_collisions_yearly_statistics['rate_victims'] = nyc_collisions_yearly_statistics['victims'] / nyc_collisions_yearly_statistics['collisions_n']
nyc_collisions_yearly_statistics['rate_deaths'] = nyc_collisions_yearly_statistics['deaths'] / nyc_collisions_yearly_statistics['collisions_n']
nyc_collisions_yearly_statistics['rate_injuries'] = nyc_collisions_yearly_statistics['injuries'] / nyc_collisions_yearly_statistics['collisions_n']
nyc_collisions_yearly_statistics['average_collision_month'] = nyc_collisions_yearly_statistics['collisions_n'] / nyc_collisions_yearly_statistics['months_n']
nyc_collisions_yearly_statistics['average_victims_month'] = nyc_collisions_yearly_statistics['victims'] / nyc_collisions_yearly_statistics['months_n']
nyc_collisions_yearly_statistics['average_deaths_month'] = nyc_collisions_yearly_statistics['deaths'] / nyc_collisions_yearly_statistics['months_n']
nyc_collisions_yearly_statistics['average_injuries_month'] = nyc_collisions_yearly_statistics['injuries'] / nyc_collisions_yearly_statistics['months_n']
nyc_collisions_yearly_statistics = nyc_collisions_yearly_statistics.drop(columns='months_n')




# Formating table for shiny app

numeric_columns_to_format = ['collisions_n',
                             'victims',
                             'deaths',
                             'injuries',
                             'average_collision_month',
                             'average_victims_month',
                             'average_deaths_month',
                             'average_injuries_month']


rates_columns_to_format  = ['rate_victims','rate_deaths', 'rate_injuries']



nyc_collisions_yearly_statistics[numeric_columns_to_format] = (
    nyc_collisions_yearly_statistics
    .filter(numeric_columns_to_format)
    .applymap(lambda x: add_commas(x)) 
    )

nyc_collisions_yearly_statistics[rates_columns_to_format] = (
    nyc_collisions_yearly_statistics
    .filter(rates_columns_to_format)
    .applymap(lambda x: four_digits(x)) 
    )
