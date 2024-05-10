import json
import requests
import datetime as dt

data = {
    "username": "Guneeti",
    "role": 10,
    "application_status":"NPS",
    "ques_1_content" : {'text' : 'my query1'},
    "ques_2_content" : {'text' : 'my query2'},
    "ques_3_content" : {'text' : 'my query3'},
}

 
r = requests.post('http://127.0.0.1:8000/app1/applications/', json = data)
 
print (type(r))
print (r)
print (r.status_code)
print (r.json())
