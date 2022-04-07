from re import I
from flask import Flask, request, make_response, jsonify  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api, Resource, fields  # Api 구현을 위한 Api 객체 import
from flask import json
import pandas as pd
from dto.job_class import job_data
from service.recommendationService import recommendation
from flask_cors import CORS

app = Flask(__name__)  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.
api = Api(app)  # Flask 객체에 Api 객체 등록
CORS(app)

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


@api.route('/rec-api/v1/surveys/results_test')  # 데코레이터 이용, '/hello' 경로에 클래스 등록
class HelloWorld(Resource):
    def post(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        rankData = []
        rankData.append(job_data(1, 1, "Websites", "", "https://i.ibb.co/tLTkY32/Web.png").__dict__)
        rankData.append(job_data(2, 2, "Utilities", "", "https://i.ibb.co/vZ9p437/Util.png").__dict__)
        rankData.append(job_data(3, 6, "Finance", "", "https://i.ibb.co/SvD3jKG/Finance.png").__dict__)
        j = job_data(3, 6, "Finance", "", "https://i.ibb.co/SvD3jKG/Finance.png")
        print(j.__dict__)
        return make_response(jsonify({"rankData": rankData}), 200)


@api.route('/rec-api/v1/surveys/results')
class recommendationService(Resource):
    @api.expect(surveyResult)
    def post(self):
        params = json.loads(request.get_data(), encoding='utf-8')

        if len(params) == 0:
            return make_response(jsonify({"code": "no_param", "message": "data 없음"}), 412)

        result = {}

        for param in params['surveyResult']:
            if param['questionInitial'] not in question_columns:
                return make_response(jsonify({"code": "columns_error", "message": "잘못된 컬럼"}), 412)
            if param['questionInitial'] != 'aboutme_dev_type' and param['answerSeq'] is None:
                return make_response(
                    jsonify({"code": "answer_error", "message": param['questionInitial'] + "가 입력되지 않았습니다."}), 412)

            result[param['questionInitial']] = [param['answerSeq']]

        if result['aboutme_dev'][0] == 2:
            if 'aboutme_dev_type' not in result:
                result['aboutme_dev_type'] = None
            else:
                return make_response(jsonify({"code": "columns_error", "message": "잘못된 컬럼"}), 412)

        if len(result) != 36:
            return make_response(jsonify({"code": "columns_error", "message": "잘못된 컬럼"}), 412)

        data = pd.DataFrame(data=result)
        try:
            result = recommendation(data)
        except Exception as e:
            return make_response(jsonify({"code": "server_error", "message": "server_error"}), 500)

        return make_response(jsonify({"rankData": result}), 200)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8083)
