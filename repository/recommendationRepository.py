import pymysql
import pandas as pd
from sqlalchemy import create_engine

db_connection_str = 'mysql+pymysql://root:bigoroot@localhost:3307/bigo_db'
db_connection = create_engine(db_connection_str)
conn = db_connection.connect()


def save_recommendation(result):
    result.to_sql(name='tb_survey_record', con=db_connection, if_exists='append', index=False)
    return


def find_job_rank(job_result):

    sql = "select * from tb_job where job_id="


    for i in range(1,4):
        job = pd.read_sql_query(sql, conn)
    rank_data = []

    return rank_data