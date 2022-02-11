from crypt import methods
import datetime
from fcntl import lockf
import json
from os import name
import random
from unittest import result
from flask import Flask

app = Flask(__name__)

with open('student_sample.json') as json_file:
    json_data = json.load(json_file)


@app.route("/")
def Welcome():
    return "<p>Welcome!</p>"
    

@app.route("/student")
def randomStudent():
    return json_data[random.randrange(0, len(json_data))]


@app.route("/student/<name>", methods=["GET"])
def get_student(name):
    name_list= list()
    for i in range(len(json_data)):
        name_list.append(json_data[i]["name"])

    if name in name_list:
        idx = int(name_list.index(name))
        return f'{name} is in the list! ID is {idx}'
    else:
        return f'{name} is not in the list.'


# ongoing
@app.route("/student/<id>", methods=["PUT"])
def update_student(id):
    return "PUT"


@app.route("/student/<name>", methods=["POST"])
def add_student(name):
    json_data[len(json_data)-1]["name"] = name
    json_data[len(json_data)-1]["id"] = random.randrange(0,100)
    return f'{name} is added in the list'


@app.route("/student/<name>/<id>", methods=["DELETE"])
def delete_student(name, id):
    name_list= list()
    for i in range(len(json_data)):
        name_list.append(json_data[i]["name"])
    
    idx = int()
    if name in name_list:
        idx = name_list.index(name)

        if json_data[idx]["id"] == id :
            del json_data[idx]
            return "Delete"
        else : 
            return "Enter another name or id."
# else의 경우 제대로 출력됨.
# 학생 리스트에 있는 name과 id 입력 시, TypeError


# 현재 시간을 반환
@app.route("/time")
def now():
    now = datetime.datetime.now()
    return now.strftime("%Y년 %m월 %d일 %H시 %M분")