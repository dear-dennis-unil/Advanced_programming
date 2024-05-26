from shiny import ui

content = ui.page_fillable(
    ui.layout_columns(
        ui.card(
            ui.card_header('Conclusions'),
            ui.p("1. There has not been an improvement from the NYPD in dealing with the specific circumstances that bring forth the car collisions in the neighbourhoods of East New York, park-cemetery \& Crown Heights North."),
            ui.p("2. Considering that the greatest number of collisions come before entering work, and because of the contributing factor of either 'Distraction' or 'Failure to Yield-right-of-way' it can be concluded that most collisions can be avoided by responsible behaviour, better time management, and/or if the City of New York offers a more efficient public transportation system."),
            ui.p("3. Even if the number of collisions has decreased the rate of victims as a by-product to collisions has increased. Therefore, the number of victims per years remains almost constant. This would mean that from a number of victims  point of view there has not been a significant improvement."),
            style="height: 70vh; display: flex; align-items: center; justify-content: center;"
            )

    )
)

