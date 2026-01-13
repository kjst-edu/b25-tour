#%%
import seaborn as sns

from data import df

from shiny import App,render,ui,reactive

import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "MS Gothic"

labels = ["治安指数" , "衛生指数" , "国際評価指数" , "気候指数"]

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_numeric("a_weight","治安",25,min=0,max=100),
        ui.input_numeric("b_weight","衛生",25,min=0,max=100),
        ui.input_numeric("c_weight","国際評価",25,min=0,max=100),
        ui.input_numeric("d_weight","気候",25,min=0,max=100),

        ui.output_ui("warning_message"),
    
        ui.input_selectize("selectize","地域を選択してください。（絞り込み）",{"ヨーロッパ":"ヨーロッパ","アジア・オセアニア":"アジア・オセアニア","アメリカ":"アメリカ","中東・アフリカ":"中東・アフリカ"},
                           multiple=True,),

        ui.input_select("国名" , "国を選択してください。（グラフが表示されます。）" , choices=df["国名"].tolist(), selected=df["国名"].iloc[0])
    ),
    ui.output_data_frame("ranking_df"),
    ui.output_plot("barplot"),
    title="世界各国の観光おすすめランキング",
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
            filtered = df[df["地域"].isin(selected)].copy()
        else:
            filtered = df.copy()
        
        # 4項目のinputを利用し，加重平均を取る
        filtered["合計スコア"] = (0.01 * input.a_weight() * filtered["治安指数"] +
                                      0.01 * input.b_weight() * filtered["衛生指数"] +
                                      0.01 * input.c_weight() * filtered["国際評価指数"] +
                                      0.01 * input.d_weight() * filtered["気候指数"] 
                                      )
        
        filtered = filtered.sort_values(by="合計スコア", ascending=False)

        filtered["順位"] = filtered["合計スコア"].rank(ascending=False,method="dense").astype(int)

        # ranking_dfの定義し直し
        ranking_df = filtered[["順位","国名","地域","合計スコア","治安指数","衛生指数","国際評価指数","気候指数"]].round(2)
        return render.DataTable(ranking_df)
    
    @reactive.calc
    def selected_row():
        return df[df["国名"] == input.国名()].iloc[0]
    
    @output
    @render.plot 
    def barplot():  
        row = selected_row()
        values = [row[l] for l in labels]

        fig, ax = plt.subplots(figsize = (5,4))
        ax.bar(labels,values)
        ax.set_ylim(0,80)
        ax.set_ylabel("スコア")
        ax.set_title(input.国名())

        return fig  

app=App(app_ui,server)
#%%