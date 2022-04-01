import pymysql
import pandas as pd
from sqlalchemy import create_engine

from dto.job_class import job_data

db_connection_str = 'mysql+pymysql://root:bigoroot@localhost:3307/bigo_db'
db_connection = create_engine(db_connection_str)


def save_recommendation(result):

    result.to_sql(name='tb_survey_record', con=db_connection, if_exists='append', index=False)
    return


def find_job_rank(job_result):
    conn = db_connection.connect()

    job_rank = job_result[0].argsort() + 1
    job_rank = job_rank.tolist()

    print("job_rank", job_rank)
    print(job_rank.index(1))
    sql = "select * from tb_job where job_id="

    rank_data = []
    for i in range(1, 4):
        job_code = job_rank.index(i) + 1
        result = pd.read_sql_query(sql + str(job_code), conn)
        print("result", result)
        job = result.to_dict('records')[0]
        print("job", job)
        rank_data.append(job_data(i, job['job_id'], job['job_name'], job['job_description'], job['job_img']).__dict__)

    return rank_data
