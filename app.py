# CRUD
#           Create, Read, Update, Delete
# Method :: POST, GET, PUT, DELETE

# 유저 정보로 hash된 id 생성

import datetime
import email
import hashlib
import json
from xmlrpc.client import Boolean
from flask import Flask, request, jsonify

app = Flask(__name__)

def openjson():
    json_file = open('student_sample.json', 'r')
    json_data = json.load(json_file)
    json_file.close()
    return json_data
# 뒤에 func에서 json_data 사용하려고 
# 매번 필요할 때마다 열어주니까 업데이트 되지 않을까(예상)


# 전체 student data 조회
@app.route("/student")
def student():
    json_file = open('student_sample.json', 'r')
    json_data = json.load(json_file)
    json_file.close()
    return jsonify(json_data)


# 입력한 name이 student data에 있는지 확인
def islist(name):
    name_list = list()
    json_data = openjson()
    for i in range(len(json_data)):
        name_list.append(json_data[i]["name"])
    if name in name_list:
        return True
    else:
        return False


# email로 hashed ID 생성
def makeID(email):
    id = hashlib.md5(bytes(email, 'utf-8')).hexdigest()
    print(id)


# name으로 index와 id 찾는 함수 -> id를 key로 설정하면 수정 필요
def find_idx(name: str):
    json_data = openjson()
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

@app.route("/studentByName/<name>", methods=["GET"])
def get_student_by_name(name):
    json_data = openjson()
    if islist(name):
        idx = find_idx(name)
        return json_data[idx]

    else:
        return f'{name} is not in the list.'

<<<<<<< HEAD

# get student data by ID
# 근데 id는 랜덤 생성 되고 있음 -> makeID()
# user : email 입력 -> hash -> get data(?)
# email로만 hashed id를 생성하는 경우, 아래 id로 data가져오기가 의미가 없지 않나?
@app.route("/student/<email>", methods=["GET"])
def get_student_by_id(email):
    # json_data = openjson()
    # id = hashlib.md5(bytes(email, 'utf-8')).hexdigest()
    # print(json_data[id])
    # return "done"
    pass

# update student info by ID
# PUT /student/jiwoochoi0304@gmail.com
@app.route("/student/<email>", methods=["PUT"])
def update_student(email):
    body = request.get_json()
    
    key_list = list(body.keys())
    
    json_data=openjson()
    
    id = hashlib.md5(bytes(email, 'utf-8')).hexdigest()
    

    # 키 리스트를 돌면서 json_data[id]의 [key]를 body[key]로 업데이트
    for i in range(len(key_list)):
        json_data[id][key_list[i]] = body[key_list[i]]

    with open("student_sample.json", 'w') as json_file:
        json.dump(json_data, json_file)

    return json.dumps(json_data)

=======
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
>>>>>>> 26a596d2fcd57ac77940050803ff37df60ddebbf

# Path param, Query param
# dict = map = hashmap = hashtable
# /university/collage/department/class/student?id=0
# https://stackoverflow.com/questions/449560/how-do-i-determine-the-size-of-an-object-in-python


@app.route("/student", methods=["POST"])
def add_student():
    body = request.get_json()
    # { "name": "jiwoo", "age": 25, "email": "jiwoochoi0304@gmail.com"}

    id = hashlib.md5(bytes(body["email"], 'utf-8')).hexdigest()

    json_data = None
    with open("student_sample.json", 'r') as json_file:
        json_data = json.load(json_file)
        json_data.append({
            "id": id,
            "name": body["name"],
            "email": body["email"]
        })

    with open("student_sample.json", 'w') as json_file:
        json.dump(json_data, json_file)

    return json.dumps(json_data)


# DELETE
@app.route("/student/<email>", methods=["DELETE"])
def delete_student(email): 
    json_data = openjson()

    for i in range(len(json_data)):
        if json_data[i]['email'] == email:
            del json_data[i]
    
    with open("student_sample.json", 'w') as json_file:
        json.dump(json_data, json_file)

    return json.dumps(json_data)  


@app.route("/time")
def now():
    now = datetime.datetime.now()
    return now.strftime("%Y년 %m월 %d일 %H시 %M분")
