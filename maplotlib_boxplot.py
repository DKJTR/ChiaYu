import matplotlib.pyplot as plt
import pandas as pd
from pylab import *

# 字型設定
from matplotlib.font_manager import FontProperties
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

big_table = pd.read_csv("C:\\Users\\DKJTR\\Desktop\\tag_score_standardize\\finished_big_table.csv")

tag1 = big_table['新聞雜誌:商業與經濟新聞'].fillna(0)
tag2 = big_table['地區:台灣北部'].fillna(0)

# 把兩個資料序列畫成 boxplot
fig = plt.figure()
graph = plt.boxplot([tag1,tag2], labels = ['新聞雜誌:商業與經濟新聞','地區:台灣北部'], sym='')
plt.boxplot([tag1,tag2], labels = ['新聞雜誌:商業與經濟新聞','地區:台灣北部'], sym='')
plt.xticks(rotation = 45)
# plt.grid(axis = 'y')


for line in graph['medians']:
    # get position data for median line
    y, x = line.get_xydata()[1] # top of median line
    # overlay median value
    text(y, x, '%.1f' % y,
         va='center') # draw above, centered

for line in graph['boxes']:
    y, x = line.get_xydata()[0] # bottom of left line
    text(y,x, '%.1f' % y,
         va='top', # centered
         ha='center')      # below
    y, x = line.get_xydata()[3] # bottom of right line
    text(y,x, '%.1f' % y,
         va='top', # centered
             ha='center')
plt.show()
