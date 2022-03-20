# CRUD
#           Create, Read, Update, Delete
# Method :: POST, GET, PUT, DELETE


from crypt import methods
import datetime
import hashlib
import json
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
def isName(name):
    name_list = list()
    json_data = openjson()
    values = json_data.values()
    for i in range(len(json_data)):
        name_list.append(values[i]["name"])
    if name in name_list:
        return True
    else:
        return False


# email로 hashed ID 생성
def makeID(email):
    id = hashlib.md5(bytes(email, 'utf-8')).hexdigest()
    print(id)


# name으로 id(key)찾는 함수 필요
def idByName(name):
    name_list = list()
    json_data = openjson()
    values = list(json_data.values())
    keys = list(json_data.keys())
    for i in range(len(json_data)):
        name_list.append(values[i]["name"])
    id = keys[name_list.index(name)]
    return id

def isName(name):
    name_list = list()
    json_data = openjson()
    values = list(json_data.values())
    for i in range(len(json_data)):
        name_list.append(values[i]["name"])
    if name in name_list:
        return True
    else:
        return False

def isID(id):
    return True if id in openjson() else False
    
    # keys = list(json_data.keys())
    # if id not in keys:
    #     return False
    # else:
    #     return True

@app.route("/")
def Welcome():
    return "<p>Welcome!</p>"


@app.route("/student/<name>", methods=["GET"])
def get_student_by_name(name):
    json_data = openjson()
    if isName(name) == False:
        return f'{name} is not found', 404
    else:
        id = idByName(name)
        return json_data[id]


@app.route("/studentID/<name>", methods=["GET"])
def idByName(name):
    if isName(name) == False:
        return f'{name} is not found', 404
    else: 
        name_list = list()
        json_data = openjson()
        values = list(json_data.values())
        keys = list(json_data.keys())
        for i in range(len(json_data)):
            name_list.append(values[i]["name"])
        id = keys[name_list.index(name)]
        return id


# get student data by ID
# 근데 id는 랜덤 생성 되고 있음 -> makeID()
@app.route("/studentById/<id>", methods=["GET"])
def get_student_by_id(id):
    json_data = openjson()
    if isID(id) == True:
        data = json_data[id]
        return data
    else: 
        return f'{id} is not found', 404

# update student info by ID
# PUT /student/id알고 있다고 가정
@app.route("/student/<id>", methods=["PUT"])
def update_student(id):
    json_data = openjson()
    if isID(id) == True:

        body = request.get_json()

        key_list = list(body.keys())


    # key_list에 있는 key에 해 json_data[id]의 [key]의 [value]를 body[key]의 [value]로 업데이트
        for i in range(len(key_list)):
            json_data[id][key_list[i]] = body[key_list[i]]

        with open("student_sample.json", 'w') as json_file:
            json.dump(json_data, json_file)

        return json.dumps(json_data)

    else: 
        return f'{id} is not found', 404

# Path param, Query param
# dict = map = hashmap = hashtable
# /university/collage/department/class/student?id=0
# https://stackoverflow.com/questions/449560/how-do-i-determine-the-size-of-an-object-in-python


@app.route("/student", methods=["POST"])
def add_student():
    body = request.get_json()
    # { "name": "longzero", "age": 26, "email": "longzero@gmail.com"}

    id = hashlib.md5(bytes(body["email"], 'utf-8')).hexdigest()

    json_data = None
    with open("student_sample.json", 'r') as json_file:
        json_data = json.load(json_file)
        json_data[id] = body

    with open("student_sample.json", 'w') as json_file:
        json.dump(json_data, json_file)

    return json.dumps(json_data)


# DELETE
@app.route("/student/<id>", methods=["DELETE"])
def delete_student(id):
    if isID(id) == True:
        json_data = openjson()
        del json_data[id]

        with open("student_sample.json", 'w') as json_file:
            json.dump(json_data, json_file)

        return json.dumps(json_data)
    else: 
        return f'{id} is not found', 404

@app.route("/time")
def now():
    now = datetime.datetime.now()
    return now.strftime("%Y년 %m월 %d일 %H시 %M분")


# json_data test
# json_data = openjson()
# print(json_data)
# print(json_data["ffa3e85d4b7673a203ced1e1cc709efb"])
