# test_flask
# pw에 hash 적용하기
# subject 리스트에 과목 추가하기
# id 랜덤하게 생성하기
# nickname 추가하기


import datetime
import json
import random
from flask import Flask, request

app = Flask(__name__)


with open('student_sample.json', 'r') as json_file:
    json_data = json.load(json_file)

# 바로 close 하는지 확인

def islist(name):
    name_list = list()
    for i in range(len(json_data)):
        name_list.append(json_data[i]["name"])
    if name in name_list:
        return True
    else:
        return False

def isID(id):
    id_list = list()
    for i in range(len(json_data)):
        id_list.append(json_data[i]["id"])
        if id in id_list:
            return True
        else:
            return False

def find_idx(name):
    name_list = list()
    for i in range(len(json_data)):
        name_list.append(json_data[i]["name"])
    idx = int(name_list.index(name))
    return idx

def find_id(name):
    for i in range(len(json_data)):
        if name == json_data[i]["name"]:
            return json_data[i]["id"]


@app.route("/")
def Welcome():
    return "<p>Welcome!</p>"

# whole data
@app.route("/student")
def student():
    return json_data


@app.route("/student/<name>", methods=["GET"])
def get_student(name):
    if islist(name):
        idx = find_idx(name)
        return json_data[idx]

    else:
        return f'{name} is not in the list.'


# update; name and id check
# subject append 하는 거 추가해야 함
@app.route("/student/<name>/<id>", methods=["PUT"])
def update_student(name, id):
    if islist(name):
        idx = find_idx(name)
        if json_data[idx]["id"] == id:
            body = request.get_json()
            # nickname&bio, only nickname, only bio 구분?
            nickname = body["nickname"]
            bio = body["bio"]

            json_data[idx]["nickname"] = nickname
            json_data[idx]["bio"] = bio
    else:
        return "enter another right name and id."

    with open("student_sample.json", 'r+') as json_file:
        json.dumps(json_data, json_file)


# name, nickname, bio만 request body에 json으로
# id = random
# subject = empty list
@app.route("/student/<name>", methods=["POST"])
def add_student(name):
    body = request.get_json()

    nickname = body["nickname"]
    bio = body["bio"]

    json_data[len(json_data)]["name"] = name
    json_data[len(json_data)]["nickname"] = nickname
    json_data[len(json_data)]["bio"] = bio
    json_data[len(json_data)]["subject"] = []

    new_id = random.randint(1,1000)       
    while isID(new_id):
        new_id = random.randint(1,10000)
        return new_id    
    json_data[len(json_data)]["id"] = new_id

    with open("student_sample.json", 'r+') as json_file:
        json.dumps(json_data, json_file)
    

@app.route("/student/<name>/<id>", methods=["DELETE"])
def delete_student(name, id):
    if islist(name):
        idx = find_idx(name)
        if json_data[idx]["id"] == id:
            del json_data[idx]
    else:
        return "Enter another name or id."

    with open("student_sample.json", 'r+') as json_file:
        json.dumps(json_data, json_file)


@app.route("/time")
def now():
    now = datetime.datetime.now()
    return now.strftime("%Y년 %m월 %d일 %H시 %M분")