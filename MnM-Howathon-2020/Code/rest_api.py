import flask
import subprocess
from flask import Flask, request
from flask_restful import Resource,Api
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import LUIS_link_chatbot_GUI

app = Flask(__name__)
##Dash app


api = Api(app)
@app.route('/run_chatbot')
def run_chatbot():
    run_bat_file()

    return "<h1> Opening the Chatbot</h1>"
    #return jsonify({"about":"Hello World"})

def run_bat_file():
    subprocess.call([r'C:\Users\aadmohan\Desktop\Howathon\Chatbot.bat'])

    return "<h1> Opening the Chatbot</h1>"

@app.route('/query-example')
def query_example():
    user_input_age = int(request.args.get('user_input_age'))
    user_input_risk = str(request.args.get('user_input_risk'))
    user_input_saving = int(request.args.get('user_input_saving'))
    user_input_EmergencyCorpus = bool(request.args.get('user_input_EmergencyCorpus'))
    user_input_income = int(request.args.get('user_input_income'))

    resp_msg = LUIS_link_chatbot_GUI.get_resp_decision_engine(user_input_age,user_input_risk,user_input_saving, user_input_EmergencyCorpus, user_input_income)
    return {"message":resp_msg}

class HelloWorld(Resource):
    def get(self,money):
        resp = "gagdf" + str(money)
        return resp
        #return {'about':'Hello World'}
    def post(self):
        some_json = request.get_json()
        return {'you sent': some_json}, 201
class Multi(Resource):
    def get(self,num):
        return {'result':num*10}

api.add_resource(HelloWorld,'/<int:money>')
api.add_resource(Multi,'/Multi/<int:num>')

if __name__ == '__main__':
    app.run(debug = True)
