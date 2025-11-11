import seaborn as sns

from data import df

from shiny import App,render,ui

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_numeric("numeric","Numeric input",1,min=0,max=100),
        ui.input

        )
    )
)