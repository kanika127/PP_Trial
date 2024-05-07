import json
import requests
import datetime as dt

data = {
    "username": "Nitish",
    "role": 19,
    "application_status":"A",
    "ques_1_content" : {'text' : 'my query1'},
    "ques_2_content" : {'text' : 'my query2'},
    "ques_3_content" : {'text' : 'my query3'},
}

 
r = requests.post('http://127.0.0.1:8000/app1/applications/', json = data)
#r = requests.post('http://localhost:8000/app1/hello/')
 
print (type(r))
print (r)
print (r.status_code)
print (r.json())
