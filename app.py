from flask import Flask, request  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api, Resource, reqparse, fields  # Api 구현을 위한 Api 객체 import
from flask import json
import pandas as pd
import tensorflow as ts
from job_class import job_data


app = Flask(__name__)  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.
api = Api(app)  # Flask 객체에 Api 객체 등록


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


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8083)