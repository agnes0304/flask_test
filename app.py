import datetime
import json
from flask import Flask

app = Flask(__name__)

@app.route("/")
def Welcome():
    return "<p>Welcome!</p>"

# 모든 method는 GET이며 response content-type은 json입니다.
# /student로 접근하면 랜덤한 student 배열을 반환
@app.route("/student")
def students():
    with open('student_sample.json') as json_file:
        json_data = json.load(json_file)
        return str(json_data)

# /hello로 접근하면 현재 시간을 반환
@app.route("/hello")
def now():
    now = datetime.datetime.now()
    return now.strftime("%Y년 %m월 %d일 %H시 %M분")