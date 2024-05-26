# Libraries
import numpy as np
import pandas as pd
import plotly.express as px

# Functions

def four_digits(x):
    return '{:,.4f}'.format(x)



# Scripts
import scripts.ps_01_data_cleansing_and_tidying as ps01


# Create a DataFrame with column names
column_names_df = pd.DataFrame({'col_names': ps01.nyc_collisions.columns}) # type: ignore
wide_names = ["street_name", "number_of", "contributing_factor", "vehicle_type"]



# Creating initial_data_summarised

initial_data_summarised = (
    pd.DataFrame({'variable_category': wide_names })
    .assign(variable_category = lambda x: x['variable_category'] + '_category',
            variable_category_n = [column_names_df.col_names.str.contains(x).sum() for x in wide_names], 
            variable_category_type = [(ps01.nyc_collisions # type: ignore
                                       .filter(regex = x)
                                       .iloc[:,0]
                                       .dtypes
                                       .name) for x in wide_names])
)


statistics_summary = (
    ps01.nyc_collisions_id
    .get(['collision_id', 'number_of_persons_injured', 'number_of_persons_killed', 'victims'])
    .melt(id_vars = 'collision_id', 
          value_vars = ['number_of_persons_injured', 'number_of_persons_killed', 'victims'], 
          var_name = 'victim_category', 
          value_name = 'victims_n')
    .groupby('victim_category')
    .agg(victim_category_mean=('victims_n', 'mean'), 
         victim_category_sd=('victims_n', 'std'))
    .reset_index()
)


# formated for shiny app
statistics_summary[['victim_category_mean', 'victim_category_sd']]= (
    statistics_summary[['victim_category_mean', 'victim_category_sd']]
    .applymap(lambda x: four_digits(x)) 
    ) 



statistics_summary_conditional = (
    ps01.nyc_collisions_id
    .query('victims >= 1 or number_of_persons_injured >= 1 or number_of_persons_killed > 1')
    .get(['collision_id', 'number_of_persons_injured', 'number_of_persons_killed', 'victims'])
    .melt(id_vars = 'collision_id',
          value_vars = ['number_of_persons_injured', 'number_of_persons_killed', 'victims'],
          var_name = 'victim_category',
          value_name = 'victims_n')
    .groupby('victim_category')
    .agg(victim_category_mean=('victims_n', 'mean'), victim_category_sd=('victims_n', 'std'))
    .reset_index()
    )

# formated for shiny app
statistics_summary_conditional[['victim_category_mean', 'victim_category_sd']]= (
    statistics_summary_conditional[['victim_category_mean', 'victim_category_sd']]
    .applymap(lambda x: four_digits(x)) 
    ) 



# Univariate visualizations
## Victims

# "fig-histograms-victims
fig_univariate_victims_plot = px.histogram(ps01.nyc_collisions_id, 
                   x = 'victims', 
                   title = "Distribution of number of victims",
                   labels = {'victims': 'Number of victims', 'count': 'Number of collisions'},
                   log_y = True, 
                   color_discrete_sequence = ['orange'], 
                   template='none')

fig_univariate_victims_plot.update_traces(marker_line_color='black', marker_line_width=1.5)



# fig-histograms-deaths
fig_univariate_deaths_plot = px.histogram(ps01.nyc_collisions_id.query('number_of_persons_killed.notnull()'), x='number_of_persons_killed', 
                   title="Distribution of number of Deaths",
                   labels={'number_of_persons_killed': 'Number of deaths', 'count': 'Number of collisions'},
                   log_y=True, 
                   color_discrete_sequence=['skyblue'],
                   template='none')

fig_univariate_deaths_plot.update_traces(marker_line_color='black', marker_line_width=1.5)


# Multivariate visualizations
# fig-bar_chart_collisions
fig_multivariate_collisions_plot = px.bar(ps01.nyc_collisions_yearly_statistics, x='accident_year', y='collisions_n',
             title="Collisions per year in NYC",
             labels={'accident_year': 'Year', 'collisions_n': 'Number of collisions'},
             color_discrete_sequence=['#008f9b'],
             template='none')

fig_multivariate_collisions_plot.update_traces(marker_line_color='black', marker_line_width=1, opacity=0.9)
fig_multivariate_collisions_plot.update_layout(template='plotly_white')


# fig-bar_chart_victims
'''
histograms_collisions_per_year_df = (
    ps01.nyc_collisions_yearly_statistics
    .drop(columns=['collisions_n', 'victims'])
    .filter(regex=r'^(?!.*rate)')
    .melt(id_vars = 'accident_year',
           value_vars = ['deaths', 'injuries'],
           var_name = 'severity_type', 
           value_name = 'severity_n') 
)

# Plot using Plotly
fig_multivariate_victims_plot = px.bar(histograms_collisions_per_year_df,
            x = 'accident_year',
            y = 'severity_n', 
            color = 'severity_type',
            title = "Low number of deaths compared to injuries",
            labels={'accident_year': 'Year', 'severity_n': 'Number of victims', 'severity_type': 'Severity'},
            color_discrete_map={'deaths': '#6667AB', 'injuries': '#5bb450'},
            barmode='stack', 
            template='none'
            )
'''

## Deaths

'''
# fig-bar_chart_deaths
fig_multivariate_deaths_plot = px.bar(ps01.nyc_collisions_yearly_statistics,
            x = 'accident_year', y = 'deaths',
            title="Number of deaths per year",
            labels={'accident_year': 'Year', 'deaths': 'Number of deaths'},
            color_discrete_sequence=['#6667AB'],
            template='none')

fig_multivariate_deaths_plot.update_traces(marker_line_color='black', marker_line_width=1, opacity=0.9)
fig_multivariate_deaths_plot.update_layout(template='plotly_white')
'''

# NYC collisions per month of accident, and coordinates
nyc_collisions_month_statistics = (
    ps01.nyc_collisions_id
    .groupby(['accident_year', 'accident_month'])
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
        rate_injuries=lambda x: x['injuries'] / x['collisions_n'],
        accident_year_2=lambda x: x['accident_year']
    )
)
