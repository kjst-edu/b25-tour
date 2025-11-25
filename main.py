#%%
import seaborn as sns

from data import df

from shiny import App,render,ui

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_numeric("a_weight","治安",1,min=0,max=100),
        ui.input_numeric("b_weight","衛生",1,min=0,max=100),
        ui.input_numeric("c_weight","混雑",1,min=0,max=100),
        ui.input_numeric("d_weight","評価",1,min=0,max=100),
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
            filtered = df[df["region"].isin(selected)].copy()
        else:
            filtered = df.copy()
        
        filtered["weighted_score"] = (input.a_weight() * filtered["a"] +
                                      input.b_weight() * filtered["b"] +
                                      input.c_weight() * filtered["c"] +
                                      input.d_weight() * filtered["d"] 
                                      )
        
        filtered = filtered.sort_values(by="weighted_score", ascending=False)

        ranking_df = filtered[["country","region","weighted_score","a","b","c","d"]].round(2)
        return render.DataTable(ranking_df)

app=App(app_ui,server)
#%%