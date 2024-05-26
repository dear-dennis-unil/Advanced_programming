from shiny import ui

content = ui.page_fillable(
    ui.layout_columns(
        ui.card(ui.p("In the last 10 years, where, when, by what reasons have there been more car accidents, and how many victims have as a by-product?"),
                style="height: 70vh; display: flex; align-items: center; justify-content: center;"          
            )

    )
)


