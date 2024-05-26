# 0.0 Importing libraries
import numpy as np
import geopandas as gpd
import plotly.express as px


# 1.0 Importing geodata
nyc_shape_file = gpd.read_file("inputs/data/aggregated_neighbourhood_data/agg_data.shp")
nyc_shape_file = nyc_shape_file.dropna(subset=['accdnt_'])
nyc_shape_file_year = [nyc_shape_file[nyc_shape_file.accdnt_ == year] for year in list(np.arange(2012, 2024))]


# 2.0 Function for ONE chropleth_map
def chropleth_map(df):
    fig = px.choropleth_mapbox(
        df,
        geojson = df,
        locations = df.index,  # Use the index to link the geometry
        color = 'victims',  # Column that contains the number of victims
        animation_frame = 'accdnt_',
        hover_name = 'ntaname',  # Column to display when hovering over a neighborhood
        mapbox_style = "carto-positron",
        center = {"lat": 40.7128, "lon": -74.0060},  # Center the map around NYC
        zoom = 10,  # Adjust zoom level as needed
        opacity = 0.5,  # Adjust the opacity of the polygons
    )

    fig.update_layout(
        title='Number of Car Victims per Neighborhood in NYC Over Time',
        margin={"r":0,"t":0,"l":0,"b":0},
        coloraxis_colorbar=dict(
            title="Victims",
        )
    )

    return fig

# 3.0 List comprehension that stores MULTIPLE chropleth_maps
figs = [chropleth_map(df_year) for df_year in nyc_shape_file_year]
