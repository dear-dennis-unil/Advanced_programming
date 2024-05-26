from shiny import ui

content = ui.page_fillable(
    ui.layout_columns(
        ui.card(
            ui.card_header('Welcome to the NYC collisions dashboard'),
            ui.p('Here we will find information from 2012 to 2023 related to the car collisions in New York City.'),
            ui.p("1.The ", ui.strong('Research questions'), "expains our goals of this research"),
            ui.p("2.In the ", ui.strong('Data'), " tab you will find data structure and missing values."),
            ui.p("3. The ", ui.strong('Data sources'), " tab shares the link to where to download the data"),
     #       ui.p("4. In the ", ui.strong("Statistics"), " tab you'll find the statistics of the data."),
            ui.p("4. The ", ui.strong("Answers"), " tab offers responds the what, where and, how of the collisions."),
            ui.p("5. In the ", ui.strong("Conclusions"), "We will mix our knowledge to form real life conclusions."),
            style="height: 70vh; display: flex; align-items: center; justify-content: center;"

    ),
        ui.card(
            ui.output_image("car_collisions_home_page_image"),
            style="height: 70vh; display: flex; align-items: center; justify-content: center;"
    )
    )
)