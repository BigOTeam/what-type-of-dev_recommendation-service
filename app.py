from flask import Flask, request  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api, Resource, fields  # Api 구현을 위한 Api 객체 import
from flask import json
import pandas as pd
from dto.job_class import job_data
from service.recommendationSevice import recommendation


app = Flask(__name__)  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.
api = Api(app)  # Flask 객체에 Api 객체 등록

surveyResult_fields = api.model('User', {
    'questionInitial': fields.String,
    'answerSeq': fields.Integer,
})


surveyResult = api.model('surveyResult', {
    'surveyResult': fields.List(fields.Nested(surveyResult_fields))
})

question_columns = ['aboutme_dev', 'aboutme_dev_type', 'aboutme_age', 'aboutme_gender',
                    'aboutme_salary', 'aboutme_work', 'aboutme_mobile', 'dev_headphone',
                    'dev_eat', 'dev_drink', 'dev_team_size', 'dev_worktime', 'moral_cctv',
                    'moral_rule', 'moral_help', 'moral_gov_protection', 'moral_manner',
                    'moral_environment', 'relation_equal', 'relation_understand',
                    'relation_humble', 'relation_friends', 'relation_region',
                    'success_own_decision', 'success_rich', 'success_recognize',
                    'success_admire', 'success_leader', 'life_good', 'life_job',
                    'life_fun', 'life_safe', 'life_givefun', 'adventure_creative',
                    'adventure_idea', 'adventure_fun']

model_question_columns = ['dev_eat', 'dev_headphone', 'dev_team_size', 'dev_worktime',
       'moral_cctv', 'life_good', 'life_job', 'life_safe', 'life_fun',
       'life_givefun', 'adventure_creative', 'adventure_fun', 'adventure_idea',
       'moral_environment', 'moral_gov_protection', 'moral_help',
       'moral_manner', 'moral_rule', 'relation_equal', 'relation_friends',
       'relation_humble', 'relation_region', 'relation_understand',
       'success_admire', 'success_leader', 'success_own_decision',
       'success_recognize', 'success_rich']

@api.route('/surveys/results_test')  # 데코레이터 이용, '/hello' 경로에 클래스 등록
class HelloWorld(Resource):
    def post(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        rankData = []
        rankData.append(job_data(1, 1, "Websites", "", "https://i.ibb.co/tLTkY32/Web.png").__dict__)
        rankData.append(job_data(2, 2, "Utilities", "", "https://i.ibb.co/vZ9p437/Util.png").__dict__)
        rankData.append(job_data(3, 6, "Finance", "", "https://i.ibb.co/SvD3jKG/Finance.png").__dict__)
        j = job_data(3, 6, "Finance", "", "https://i.ibb.co/SvD3jKG/Finance.png")
        print(j.__dict__)
        return {"rankData": rankData}


@api.route('/surveys/results')
class recommendationService(Resource):
    @api.expect(surveyResult)
    def post(self):
        params = json.loads(request.get_data(), encoding='utf-8')
        print(params)
        if len(params) == 0:
            return 'No parameter'

        params_str = ''
        result = {}

        for param in params['surveyResult']:
            print(param)
            if param['questionInitial'] not in question_columns:
                break
            if param['questionInitial'] != 'aboutme_dev_type' and param['answerSeq'] is not None:
                result[param['questionInitial']] = [param['answerSeq']]

        print(result)
        print(result.keys())
        print(len(result))
        data = pd.DataFrame(data=result)
        print(data)
        model_question = data[model_question_columns]
        print(model_question)
        print(recommendation(model_question))
        return params_str

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8083)