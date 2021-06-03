#import MySQLdb
import pymysql
from sqlalchemy import create_engine
def getdb():
    '''
    db1 = MySQLdb.connect(host="139.59.57.188",    # your host, usually localhost
                         port=3306,         # port for mysql
                         user="akdharia",         # your username
                         passwd="b3bf869f7b",  # your password
                         db="navposmod")        # name of the data base
    '''
    db1 = pymysql.connect(host="139.59.57.188",    # your host, usually localhost
                         port=3306,         # port for mysql
                         user="akdharia",         # your username
                         passwd="b3bf869f7b",  # your password
                         db="navposmod")        # name of the data base
    return db1

def writedb(df,db,table_name,flag):
    engine = create_engine("mysql+mysqldb://akdharia:b3bf869f7b@139.59.57.188/"+str(db)+"")
    df.to_sql(name=str(table_name), con=engine, if_exists='append', index=flag, chunksize = 1000, index_label=None)
    engine.dispose()
