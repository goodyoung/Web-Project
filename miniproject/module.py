import pymysql
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


def first():
    conn = pymysql.connect(host = "localhost", user="root", passwd="rjsdud", db ="study", charset = "utf8")
    sql = '''
    select * from user_id
    '''
    df = pd.read_sql(sql,conn)
    return df

def insertuser(real_name,name,psw):
    conn = pymysql.connect(host = "localhost", user="root", passwd="rjsdud", db ="study", charset = "utf8")
    cur = conn.cursor()
    sql = f"insert into user_id(name,userid,psw) values (\"{real_name}\",\"{name}\",\"{psw}\")"
    cur.execute(sql)
    conn.commit()

def leaderboard():
    conn = pymysql.connect(host = "localhost", user="root", passwd="rjsdud", db ="study", charset = "utf8")
    sql = '''
    select * from user_id
    '''
    df = pd.read_sql(sql,conn)

    dic = df[['name','Lv','Exp']].sort_values(by=['Lv','Exp'],ascending=False)
    dic = dic.T.to_dict()
    return dic