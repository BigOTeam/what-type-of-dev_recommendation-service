import tensorflow as tf
import pandas as pd

def recommendation(data):
    model = tf.keras.models.load_model('model/dnn_estate_sigmoid.h5')

    # test data에 대한 예측값
    y_pred = model.predict(data)

    print(y_pred)
    y_result = pd.DataFrame(y_pred)
    y_result.columns = ['job_website', 'job_utilities', 'job_database', 'job_system_software',
                        'job_it_infrastrucutre', 'job_frinance', 'job_data_science',
                        'job_programming_tools', 'job_enetertainment', 'job_games']
    return y_result
