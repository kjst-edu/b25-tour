
import seaborn as sns

from data import df

from shiny import App,render,ui

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_numeric("numeric","治安",1,min=0,max=100),
        ui.input_numeric("numeric","衛生",1,min=0,max=100),
        ui.input_numeric("numeric","混雑",1,min=0,max=100),
        ui.input_numeric("numeric","評価",1,min=0,max=100),
        ui.input_selectize("slectize","地域を選択してください。",{"europe":"ヨーロッパ","asia":"アジア・オセアニア","america":"アメリカ","africa":"中東・アフリカ"})

    ),
    ui.output_data_frame("ranking.df"),
    title="観光"
)


app=App(app_ui,None)