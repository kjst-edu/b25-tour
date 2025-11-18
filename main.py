#%%
import seaborn as sns

from data import df

from shiny import App,render,ui

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_numeric("numeric","治安",1,min=0,max=100),
        ui.input_numeric("numeric","衛生",1,min=0,max=100),
        ui.input_numeric("numeric","混雑",1,min=0,max=100),
        ui.input_numeric("numeric","評価",1,min=0,max=100),
        ui.input_selectize("selectize","地域を選択してください。",{"europe":"ヨーロッパ","asia":"アジア・オセアニア","america":"アメリカ","africa":"中東・アフリカ"},
                           multiple=True,),

    ),
    ui.output_data_frame("ranking_df"),
    title="観光",
)


def server(input,output,session):
    @render.data_frame
    def ranking_df():
         # ★ 選択された地域リストを取得
        selected = input.selectize()

        # ★ 地域が選ばれていればフィルタ、選ばれていなければ全部
        if selected:
            filtered = df[df["region"].isin(selected)]
        else:
            filtered = df
        return render.DataTable(filtered)

app=App(app_ui,server)
#%%