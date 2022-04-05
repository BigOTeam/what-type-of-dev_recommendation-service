import pymysql
import json
import pandas as pd
from sqlalchemy import create_engine
from dto.job_class import job_data

with open("config.json", 'r') as f:
    db_confing = json.load(f)
    print("db", db_confing)
db_connection_str = 'mysql+pymysql://' + db_confing['user'] + ":" + db_confing["password"] + "@" \
                    + db_confing["HOST"] + ":" + db_confing["port"] + "/" + db_confing["SCHEMA"]
db_connection = create_engine(db_connection_str)

job_name = {"Websites": "웹개발자",
       "Utilities": "유틸 소프트웨어 개발자",
       "Database": "DB 엔지니어",
       "SystemSoftware": "OS 개발자",
       "ITInfrastructure": "인프라 엔지니어",
       "Finance": "금융권 개발자",
       "DataScience": "데이터 엔지니어",
       "ProgrammingTools": "개발툴 개발자",
       "Entertainment": "엔터테인먼트 개발자",
       "Game": "게임 개발자"}


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

        print("job_rank", job_rank)
        print(job_rank.index(1))
        sql = "select * from tb_job where job_id="

        for i in range(1, 4):
            job_code = job_rank.index(i) + 1
            result = pd.read_sql_query(sql + str(job_code), conn)
            print("result", result)
            job = result.to_dict('records')[0]
            print("job", job)
            rank_data.append(
                job_data(i, job['job_id'], job_name[job['job_name']], job['job_description'], job['job_img']).__dict__)
    except Exception as e:
        print(e)
        raise

    return rank_data
