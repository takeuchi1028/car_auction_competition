import streamlit as st
import pandas as pd

from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score

# Load the data
df_ans = pd.read_csv('test.csv')

# 目的変数の変数名
colunm_name = 'sellingprice'

st.title('Used Car Auction Prices Competition')
ranking_df = pd.read_csv('ranking.csv')

st.sidebar.title('オプション')
st.sidebar.write('ランキングボードを並び替えする基準とする評価指標を選択してください。')
option = ['平均二乗誤差 (MSE)', '平均絶対誤差 (MAE)', '決定係数 (R2)']
selected_score = st.sidebar.selectbox('Select your option', option)
st.sidebar.write('ランキングボードの結果を CSV ファイルで出力したい場合')
st.subheader('CSV ファイルを提出')

# streamlitでテキストを入力
name = st.text_input('ニックネームを入力してください。')
group_name = st.text_input('グループ名を入力してください。')

# streamlitでファイルをアップロード
uploaded_file = st.file_uploader("CSV ファイルをアップロードしてください。", type="csv")

# 表のアップロード方法についてサンプルを提示
st.write('提出する CSV ファイルは以下の形式で提出してください。インデックス列は不要です。')
df = pd.DataFrame({'sellingprice': [23500, 26400, 13800, 15200]})
st.dataframe(df)


# アップロードしたファイルを読み込み
st.write('CSV ファイルを選択したら以下の「評価」ボタンをクリックしてください。')
try:
    if st.button('評価') and uploaded_file is not None:

        # 読み込み
        input_df = pd.read_csv(uploaded_file)

        score_mse = round(mean_squared_error(df_ans[colunm_name], input_df[colunm_name]), 4)
        score_mae = round(mean_absolute_error(df_ans[colunm_name], input_df[colunm_name]), 4)
        score_r2 = round(r2_score(df_ans[colunm_name], input_df[colunm_name]), 4)

        df_score = pd.DataFrame({'Name': [name],
                                'Group': [group_name],
                                '平均二乗誤差 (MSE)': [score_mse],
                                '平均絶対誤差 (MAE)': [score_mae],
                                '決定係数 (R2)': [score_r2]})
        
        # ranking_df に df_score と同じ行があれば
        if ranking_df[ranking_df['Name'] == name].empty:
            ranking_df = pd.concat([ranking_df, df_score], axis=0)
        
        ranking_df.to_csv('ranking.csv', index=False)
        # print(df_score)
        st.write('推論できました！ランキングボードを確認してみましょう。')
except:
    st.write('<span style="color:red">エラーが発生したため正しく推論結果を保存できませんでした。提出フォーマット等を再度確認してみましょう。</span>', unsafe_allow_html=True)

st.sidebar.download_button('csvファイルを出力', ranking_df.to_csv(index=False), 'ranking.csv')

# st.sidebar.write('ランキングボードの結果を削除する場合')
# cleared_num = st.sidebar.number_input('消去するインデックスを入力', min_value=0)
# if st.sidebar.button('消去'):
#     ranking_df = ranking_df.drop(index=cleared_num)
#     ranking_df.to_csv('ranking.csv', index=False)

ranking_df = ranking_df.sort_values(selected_score, ascending=False)
rank = ranking_df[selected_score].rank(method='min', ascending=False).astype(int)
ranking_df.insert(0, 'Rank', rank)
ranking_df = ranking_df.sort_values('Rank', ascending=True)
ranking_df = ranking_df.reset_index(drop=True)

st.subheader('ランキングボード')
st.table(ranking_df)

# # DataFrameをHTMLに変換し、インデックスを非表示にする
# df_html = ranking_df.to_html(index=False)

# # HTMLを表示
# st.write(df_html, unsafe_allow_html=True)