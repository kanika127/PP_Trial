import json
import requests
 
data = {"ques_id": 10}
 
#r = requests.post('http://127.0.0.1:8000/gobbled_myapp/four/', json = data)
r = requests.post('http://localhost:8000/app1/hello/')
 
print (type(r))
print (r)
print (r.status_code)
print (r.json())

