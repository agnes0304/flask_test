from crypt import methods
import datetime
from fcntl import lockf
import json
from os import name
import random
from unittest import result
from flask import Flask

app = Flask(__name__)

with open('student_sample.json', 'a') as json_file:
    json_data = json.load(json_file)


def islist(name):
    name_list = list()
    for i in range(len(json_data)):
        name_list.append(json_data[i]["name"])

    if name in name_list:
        return True
    else:
        return False


def find_idx(name):
    name_list = list()
    for i in range(len(json_data)):
        name_list.append(json_data[i]["name"])
    idx = int(name_list.index(name))
    return idx


@app.route("/")
def Welcome():
    return "<p>Welcome!</p>"


@app.route("/student")
def randomStudent():
    return json_data[random.randrange(0, len(json_data))]


@app.route("/student/<name>", methods=["GET"])
def get_student(name):
    if islist(name):
        idx = find_idx(name)
        return f'{name} is in the list! ID is {idx+1}'

    else:
        return f'{name} is not in the list.'


# ongoing
@app.route("/student/<name>/<id>", methods=["PUT"])
def update_student(name, id):
    if islist(name):
        idx = find_idx(name)
        json_data[idx]["id"] = id
        json_data.dump(json_data, json_file)
        return f'ID of {name} is updated to {id}'
    else:
        return "enter another right name and id."


@app.route("/student/<name>", methods=["POST"])
def add_student(name):
    json_data[len(json_data)-1]["name"] = name
    json_data[len(json_data)-1]["id"] = random.randrange(0, 100)
    return f'{name} is added in the list'


@app.route("/student/<name>/<id>", methods=["DELETE"])
def delete_student(name, id):
    if islist(name):
        idx = find_idx(name)
        # print(idx)
        # print(json_data[idx])
        # print(json_data[idx]["id"])
        if json_data[idx]["id"] == id:
            del json_data[idx]
    else:
        return "Enter another name or id."
# "/student/h/7"의 idx, json_data[idx] 출력 결과 : 7, {'name':'h', 'id':8} 제대로 나옴


# 현재 시간을 반환
@app.route("/time")
def now():
    now = datetime.datetime.now()
    return now.strftime("%Y년 %m월 %d일 %H시 %M분")
