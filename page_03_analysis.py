from shiny import ui
from shinywidgets import output_widget  

content = (
    ui.navset_card_tab(
        ui.nav_panel("Where?",
                    ui.navset_pill(
                        ui.nav_panel('Map',
                            ui.layout_columns(
                                ui.card(  
                                    ui.input_slider("slider", "Year", 2012, 2023, 2012)
                                ),  
                                col_widths=(3,)
                            ), 
                            ui.layout_columns(
                                ui.card(output_widget('map_plotly'),
                                        style="height: 75vh; display: flex; justify-content: center;"
                                )
                            )
                        ), 
                        ui.nav_panel("Data",
                            ui.card(ui.output_data_frame('where_df'))
                        )
                    )
        ),
        ui.nav_panel('When?',
                     ui.navset_pill(
                        ui.nav_panel('History',
                                        ui.card(output_widget('year_facet'),
                                              style="align-items: center; justify-content: center;"
                                        )
                        ),
                        ui.nav_panel('Hour of the day',
                                        ui.card(output_widget('violin_plots_plotly'),
                                              style="height: 70vh; display: flex"
                                        )
                        ),
                        ui.nav_panel('Day of the week',
                                        ui.card(output_widget('boxplot_plotly'),
                                                style="height: 70vh; display: flex"
                                        )
                        )
                     )
        ),
        ui.nav_panel('Why?',
                     ui.layout_columns(
                         ui.card(ui.output_data_frame('why_df')
                        )      
                    )
        ),
        ui.nav_panel('How many?', 
                     ui.layout_column_wrap(
                         ui.card(
                             ui.output_data_frame("how_many_df")
                        )
                    )
        )
    )
)

