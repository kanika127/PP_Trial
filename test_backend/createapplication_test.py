import json
import requests
import datetime as dt

data = {
    "username": "Pradeep",
    "role": 12,
    "ques" : "my query",
    "application_status":"A"
}

 
r = requests.post('http://127.0.0.1:8000/app1/applications', json = data)
#r = requests.post('http://localhost:8000/app1/hello/')
 
print (type(r))
print (r)
print (r.status_code)
print (r.json())
