import tensorflow as tf
import pandas as pd
from repository.recommendationRepository import save_recommendation, find_job_rank

model_question_columns = ['dev_eat', 'dev_headphone', 'dev_team_size', 'dev_worktime',
       'moral_cctv', 'life_good', 'life_job', 'life_safe', 'life_fun',
       'life_givefun', 'adventure_creative', 'adventure_fun', 'adventure_idea',
       'moral_environment', 'moral_gov_protection', 'moral_help',
       'moral_manner', 'moral_rule', 'relation_equal', 'relation_friends',
       'relation_humble', 'relation_region', 'relation_understand',
       'success_admire', 'success_leader', 'success_own_decision',
       'success_recognize', 'success_rich']

model = tf.keras.models.load_model('model/dnn_estate_sigmoid.h5')


def recommendation(data):

    try:
        model_question = data[model_question_columns]

        # test data에 대한 예측값
        job_pred = model.predict(model_question)

        job_rank = find_job_rank(job_pred)
        print(job_pred)
        job_result = pd.DataFrame(job_pred)
        job_result.columns = ['job_website', 'job_utilities', 'job_database', 'job_system_software',
                            'job_it_infrastructure', 'job_finance', 'job_data_science',
                            'job_programming_tools', 'job_entertainment', 'job_games']

        survey_result = pd.concat([data, job_result], axis=1)
        save_recommendation(survey_result)

    except Exception as e:
        print(e)
        raise
    return job_rank
