import pymysql
import json
import pandas as pd
from sqlalchemy import create_engine
from dto.job_class import job_data

with open("config.json", 'r') as f:
    db_confing = json.load(f)

db_connection_str = 'mysql+pymysql://' + db_confing['user'] + ":" + db_confing["password"] + "@" \
                    + db_confing["HOST"] + ":" + db_confing["port"] + "/" + db_confing["SCHEMA"]
db_connection = create_engine(db_connection_str)

with open("job.json", 'r', encoding='UTF8') as j:
    job_name = json.load(j)



def save_recommendation(result):
    try:
        result.to_sql(name='tb_survey_record', con=db_connection, if_exists='append', index=False)
    except Exception as e:
        print(e)
        raise
    return


def find_job_rank(job_result):
    rank_data = []
    try:
        conn = db_connection.connect()

        job_rank = job_result[0].argsort() + 1
        job_rank = job_rank.tolist()

        sql = "select * from tb_job where job_id="

        for i in range(1, 4):
            job_code = job_rank.index(i) + 1
            result = pd.read_sql_query(sql + str(job_code), conn)

            job = result.to_dict('records')[0]

            rank_data.append(
                job_data(i, job['job_id'], job_name[job['job_name']], job['job_description'], job['job_img']).__dict__)
    except Exception as e:
        print(e)
        raise

    return rank_data
