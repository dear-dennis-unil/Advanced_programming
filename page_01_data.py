from shiny import ui
from shinywidgets import output_widget, render_widget  

content = (
    ui.layout_columns(
        ui.layout_columns(
            ui.card(
                ui.card_header("Raw data"),
                ui.output_data_frame("meta_data_raw"),
                full_screen=True,
                    ),
            ui.card(
                ui.card_header("Snake case data"),
                ui.output_data_frame("meta_data_tidy"),
                full_screen=True,
                )
        ),
        ui.navset_card_tab(  
            ui.nav_panel(
                "Missing information summary", 
                ui.output_data_frame("missing_info_df")  # Plot 1
            ),
            ui.nav_panel(
                "Missing Information plot", 
                output_widget("missing_info_plot")  # Plot 2
            )
        ) 
    ), 
    ui.navset_card_tab(
        ui.nav_panel('Raw data preview', ui.output_data_frame("raw_data_preview")),
        ui.nav_panel('Snake case data preview', ui.output_data_frame("tidy_data_preview")) 
    )
)
