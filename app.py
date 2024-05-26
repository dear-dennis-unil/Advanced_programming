# 0.0 Libraries, modules and scripts -----------------------------
# 0.1 Shiny Library ----------------------------------------------
from shiny import App, reactive, render, ui, run_app
from shinywidgets import output_widget, render_widget  
from shinyswatch import theme

# 0.2 ui pages ----------------------------------------------------
import page_00_01_home as page_home
import page_00_02_rq as page_rq
import page_01_data as page_data
import page_01_02_data_sources as page_data_sources

import page_03_analysis as page_analysis
import page_04_conclusions as page_conclusions


# 0.3 Scripts -----------------------------------------------------
import scripts.ps_01_data_cleansing_and_tidying as ps01
import scripts.ps_02_exploratory_data_analysis as  ps02
import scripts.ps_03_map as  ps03
import scripts.ps_04_analysis as ps04


# 0.4 Importing modules -------------------------------------------
import numpy as np
import pandas as pd
from dataprep.clean import clean_headers
from datetime import date, datetime
import plotly.express as px
import geopandas as gpd # To import shp type files
from ridgeplot import ridgeplot # For the ridgeplot
from ridgeplot.datasets import load_probly
import geopandas as gpd # to import geopandas map



# 1.0 User interface -----------------------------------------------

app_ui = ui.page_navbar(
    ui.nav_panel("Home", page_home.content),
    ui.nav_panel("Research questions", page_rq.content),
    ui.nav_panel("Data", page_data.content),
    ui.nav_panel("Data sources", page_data_sources.content),
   # ui.nav_panel("Statistics", page_statistics.content),
    ui.nav_panel("Answers", page_analysis.content),
    ui.nav_panel("Conclusions", page_conclusions.content),
    title = "New York Collisions", 
    fillable = True


)


# 2.0 Server -------------------------------------------------------
def server(input, output, session):
    # page_00_home
     @render.image
     def car_collisions_home_page_image():
         from pathlib import Path

         dir = Path(__file__).resolve().parent
         img = {"src": 'www/car_collisions_home_page.jpeg','width': '750'}
         return img
     
    # page_01_data
     @render.data_frame
     def missing_info_df():
          return (
              ps01.nyc_collisions_id_missing_filtered
              .rename(columns = {'variable': 'Variable', 
                                 'non_missing_values_n' : 'Non missing values',
                                 'missing_values_n' : 'Missing values',
                                 'missing_values_percentage' : 'Percentage of Missing values'})
                  )
     
     @render_widget
     def missing_info_plot():
          return ps01.fig_lollipop.update_layout(margin=dict(l=200, b = 100))

     @render.data_frame
     def raw_data_preview():
          return ps01.nyc_collisions_original
     

     @render.data_frame
     def tidy_data_preview():
          return  ps01.nyc_collisions_id_head 
     
    # page_02_statistics
    # first row

     @render.data_frame
     def meta_data_raw():
         return ps01.schema_df
     
     @render.data_frame
     def meta_data_tidy():
         return ps01.clean_schema_df


     
    # Page_04 analysis
     @render_widget
     def map_plotly():
        return ps03.figs[input.slider() - 2012]
     
     @render_widget
     def year_facet():
         return ps04.fig_facet.update_layout(margin=dict(l=100, r=100, t=100, b=100))
     
     @render_widget
     def violin_plots_plotly():
         return ps04.fig_violin_plots.update_layout(margin=dict(l=100, r=100, t=100, b=100))

     @render_widget
     def boxplot_plotly():
         return ps04.fig_boxplot.update_layout(margin=dict(l=100, r=100, t=100, b=100))

     @render.data_frame
     def where_df():
          return (
              ps04.top_3_victims
              .rename(columns = {'accdnt_' : 'Year of accident', 
                                 'ntaname': 'Neighbourhood', 
                                 'victims': 'Number of victims'})
                  )
     
     @render.data_frame
     def why_df():
          return (
              ps04.nyc_collisions_why
              .rename(columns = {'contributing_factor' : 'Contributing factor', 
                                 'n': 'Count'})
                  )
     
     @render.data_frame
     def how_many_df():
          return (
              ps04.nyc_collisions_yearly_statistics
              .rename(columns = {'accident_year': 'Year',
                                'collisions_n': 'Collisions',
                                'victims': 'Victims',
                                'deaths': 'Deaths',
                                'injuries': 'Injuries',
                                'rate_victims': 'Rate of victims',
                                'rate_deaths': 'Rate of deaths', 
                                'rate_injuries': 'Rate of Injuries',
                                'average_collision_month': 'Avg collision per month', 
                                'average_victims_month': 'Avg victims per month',
                                'average_deaths_month': 'Avg deaths per month', 
                                'average_injuries_month': 'Avg injuries per month'})
            
            )



# 3.0 App ----------------------------------------------------
app = App(app_ui, server)

