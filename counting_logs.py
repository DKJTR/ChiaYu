import pymysql
import paramiko
import pandas as pd
import random
from paramiko import SSHClient
from sshtunnel import SSHTunnelForwarder
from os.path import expanduser
import datetime
from datetime import timedelta

mypkey = paramiko.RSAKey.from_private_key_file("*********") # 請自行放置金鑰路徑
sql_hostname = "127.0.0.1"
sql_username = "read_only"
sql_password = # 請打入密碼
sql_main_database = 'dmp_stat'
sql_port = 3306
ssh_host = # 請輸入 伺服器位置
ssh_user = "root"
ssh_port = 22

# Raw 這邊要有的主要欄位是 source, site_id, url_pattern(人工辨識出來，要塞在 url like "%OOOOOO%" 裡面的東西)

raw = pd.read_csv("C:\\Users\\DKJTR\\Desktop\\url_label_table_joygogo.csv")

# 以下的這段 script 就會去統計... 如果有 url_pattern -> 根據 source, site_id 以及 url_pattern 進行 0422 資料撈取
# 如果沒有 url_pattern -> 僅根據 source 以及 site_id

for index, row in raw.iterrows():
    with SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_pkey=mypkey,
            remote_bind_address=(sql_hostname, sql_port)) as tunnel:
        conn = pymysql.connect(host='127.0.0.1', user=sql_username,
                               passwd=sql_password, db=sql_main_database,
                               port=tunnel.local_bind_port)
        if raw.iloc[index]['url_pattern'] is np.nan:
            raw.loc[index, ['Jack_Result']] = "Skip"
        else:
            query = '''select count(*) from dmp_stat.20190422 where `source` = "%s" and `site_id` = %s and `url` like "%%%s%%"''' % (
            raw.iloc[index]['source'], raw.iloc[index]['site_id'], str(raw.iloc[index]['url_pattern']))
            data = pd.read_sql_query(query, conn)
            raw.loc[index, ['Jack_Result']] = data.iloc[0]['count(*)']
