from shiny import ui

content = ui.page_fillable(
    ui.layout_columns(
        ui.card(
            ui.p(ui.strong('New York Motor vehicles Collision Dataset')),
            ui.p("https://www.kaggle.com/datasets/tush32/motor-vehicle-collisions-crashes"),
            ui.p(ui.strong('New York City shapefile')),
            ui.p("https://data.cityofnewyork.us/Housing-Development/Shapefiles-and-base-map/2k7f-6s2k"),
                style="height: 70vh; display: flex; align-items: center; justify-content: center;"          
            )

    )
)


