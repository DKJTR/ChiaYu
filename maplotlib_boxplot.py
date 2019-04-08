import matplotlib.pyplot as plt
import pandas as pd
from pylab import *

# 字型設定
from matplotlib.font_manager import FontProperties
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

big_table = pd.read_csv("C:\\Users\\DKJTR\\Desktop\\tag_score_standardize\\log2_square_tf_idf_result.csv")
big_table.fillna(0, inplace = True)
tag1 = big_table['Log2(TF)_square_Log2(IDF)-新聞雜誌:商業與經濟新聞']
tag2 = big_table['Log2(TF)_square_Log2(IDF)-地區:台灣北部']
tag3 = big_table['Log2(TF)_square_Log2(IDF)-新聞雜誌:地方新聞']
tag4 = big_table['Log2(TF)_square_Log2(IDF)-地區:日本']
tag5 = big_table['Log2(TF)_square_Log2(IDF)-展覽:商務貿易']
tag6 = big_table['Log2(TF)_square_Log2(IDF)-地區:歐美']
tag7 = big_table['Log2(TF)_square_Log2(IDF)-生涯階段:工作階段(青壯年)']
tag8 = big_table['Log2(TF)_square_Log2(IDF)-新聞雜誌:國際新聞']
tag9 = big_table['Log2(TF)_square_Log2(IDF)-地區:台灣南部']
tag10 = big_table['Log2(TF)_square_Log2(IDF)-旅遊:國內旅遊']


# 把資料序列畫成 boxplot
fig = plt.figure()
graph = plt.boxplot([tag1,tag2, tag3, tag4, tag5, tag6, tag7, tag8 ,tag9, tag10], labels = ['新聞雜誌:商業與經濟新聞',
                                                                                            '地區:台灣北部','新聞雜誌:地方新聞',
                                                                                            '地區:日本','展覽:商務貿易',
                                                                                            '地區:歐美','生涯階段:工作階段(青壯年)',
                                                                                            '新聞雜誌:國際新聞','地區:台灣南部',
                                                                                            '旅遊:國內旅遊'], sym='')
plt.boxplot([tag1,tag2, tag3, tag4, tag5, tag6, tag7, tag8 ,tag9, tag10], labels = ['新聞雜誌:商業與經濟新聞',
                                                                                            '地區:台灣北部','新聞雜誌:地方新聞',
                                                                                            '地區:日本','展覽:商務貿易',
                                                                                            '地區:歐美','生涯階段:工作階段(青壯年)',
                                                                                            '新聞雜誌:國際新聞','地區:台灣南部',
                                                                                            '旅遊:國內旅遊'], sym='')
plt.xticks(rotation = 45)
# plt.grid(axis = 'y')

for line in graph['medians']:
    # get position data for median line
    x, y = line.get_xydata()[0] # left of median line
    # overlay median value
    text(x, y, '%.1f' % y,
         ha='left')

for line in graph['boxes']:
    x, y = line.get_xydata()[0] # bottom of left line
    text(x, y, '%.1f' % y,
         va='bottom',
         ha='left')
    x, y = line.get_xydata()[3] # bottom of right line
    text(x, y, '%.1f' % y,
         va='bottom', # centered
             ha='left')
for line in graph['whiskers']:
    x, y = line.get_xydata()[1] # bottom of left line
    text(x, y, '%.1f' % y,
         va='bottom',
         ha='left')


plt.title("Top 10 Tags box plot")
plt.show()
plt.savefig("C:\\Users\\DKJTR\\Desktop\\tag_score_standardize\\tf_square_idf_result.png")

# Random Profile and Plotting
# import random
# x = random.randint(0,500000)
# print("The random picked profile index is..."+str(x))
raw = pd.read_csv("C:\\Users\\DKJTR\\Desktop\\tag_score_standardize\\big_table_original_table_result.csv")
tf_idf = pd.read_csv("C:\\Users\\DKJTR\\Desktop\\tag_score_standardize\\log2_tf_log2_idf_result.csv")
tf_idf.drop(['Unnamed:0'], axis = 1, inplace = True)
plt.interactive(False) # Necessary for PyCharm built-in plot shower
index = 368408
x_profile = tf_idf.iloc[index] # 334 is for original scores
x_profile = x_profile.dropna().sort_values(ascending = False)
x_profile.plot.bar()
plt.show()

x_profile_10 = x_profile.head(10).to_frame(name = 'tf_idf_score')
for i in x_profile_10.index:
    indexer = i.split("-")[1]
    x_profile_10.loc[i,'Original Ranking'] = raw.iloc[index].dropna().rank(ascending = False, method = 'min')[indexer]
print(x_profile_10)





# plt.show(block = True) # Necessary for Windows pop-out matplotlib
#
#
# # Building the table
# for i in log2_tf_table.columns:
#     column_name = "Log2(TF)_Log2(IDF)-" + i.split("[Log2(TF)]")[1]
#     row_index = i.split("[Log2(TF)]")[1]
#     log2_tf_idf_table[column_name] = log2_tf_table[i] * idf['IDF(log2N-log2d)'][row_index]

# 高中低度關注產生器
def attention_count(df):
    '''
    此功能用來計算高中低度關注
    :param df: 一列一個 uid，每一欄則為一個標籤分數
    :return: 高、中、低 度關注的各標籤數計算結果
    '''
    result_df = pd.DataFrame()
    for index, row in df.iterrows():
        interm = df.loc[index].rank(ascending = False).to_frame(name = 'ranking')
        row_rank = len(interm['ranking'].dropna())
        column_name = str(index)
        interm[column_name] = interm['ranking'].apply(lambda row: rank_trans(row,row_rank))
        interm.drop(['ranking'],axis = 1,inplace = True)
        interm = interm.transpose()
        result_df = pd.concat([result_df,interm],join = 'outer', axis = 0, sort = False)
    ranking_table = pd.DataFrame()
    for i in result_df.columns:
        ranking_table = pd.concat([ranking_table,result_df[i].value_counts().to_frame()], join = 'outer', axis = 1, sort = False)
    return ranking_table




# 排名產生器
def rank_trans(rank,total_rank):
    if rank <= total_rank/3:
        return "H"
    elif rank <= total_rank*2/3:
        return "M"
    elif rank <= total_rank:
        return "L"
    else:
        return np.nan