#%%
import seaborn as sns

from data import df

from shiny import App,render,ui

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_numeric("a_weight","治安",25,min=0,max=100),
        ui.input_numeric("b_weight","衛生",25,min=0,max=100),
        ui.input_numeric("c_weight","混雑",25,min=0,max=100),
        ui.input_numeric("d_weight","評価",25,min=0,max=100),

        ui.output_ui("warning_message"),
    
        ui.input_selectize("selectize","地域を選択してください。",{"europe":"ヨーロッパ","asia":"アジア・オセアニア","america":"アメリカ","africa":"中東・アフリカ"},
                           multiple=True,),
    ),
    ui.output_data_frame("ranking_df"),
    title="観光",
)


def server(input,output,session):
    @render.ui
    def warning_message():
        # 4つの入力値を取得
        total_weight = (
            input.a_weight() + 
            input.b_weight() + 
            input.c_weight() + 
            input.d_weight()
        )
        
        # 合計が100でない場合、警告メッセージを返す
        if total_weight != 100:
            return ui.div(
                ui.p(f"＊入力値の合計が100ではないため，正確なランキングが作成されない場合があります。現在の入力値の合計：{total_weight}", 
                      style="color: red; font-size: 85%; ")
            )
        # 合計が100であれば何も表示しない
        return None

    @render.data_frame
    def ranking_df():
         # 選択された地域リストを取得
        selected = input.selectize()

        # 地域が選ばれていればフィルタ、選ばれていなければ全部
        if selected:
            filtered = df[df["region"].isin(selected)].copy()
        else:
            filtered = df.copy()
        
        # 4項目のinputを利用し，加重平均を取る
        filtered["weighted_score"] = (0.01 * input.a_weight() * filtered["a"] +
                                      0.01 * input.b_weight() * filtered["b"] +
                                      0.01 * input.c_weight() * filtered["c"] +
                                      0.01 * input.d_weight() * filtered["d"] 
                                      )
        
        filtered = filtered.sort_values(by="weighted_score", ascending=False)

        # ranking_dfの定義し直し
        ranking_df = filtered[["country","region","weighted_score","a","b","c","d"]].round(2)
        return render.DataTable(ranking_df)

app=App(app_ui,server)
#%%