import mysql.connector
import pymysql
from sqlalchemy import create_engine
from data import df

# con = mysql.connector.connect(
#     host='127.0.0.1',
#     port=3306,
#     user='root',
#     password='Soumya@12345',
#     database='flipcart_data'
# )

engine = create_engine("mysql+pymysql://root:Soumya%4012345@127.0.0.1:3306/flipcart_data")

df.to_sql('mobile_data', con=engine, if_exists='replace', index=False)


