import json
import requests
import datetime as dt

data = {
    "username": "Kanika",
    "title": "pj#1 title",
    "medium": "pj#1 medium",
    "approx_completion_date" : dt.datetime.today().strftime('%Y-%m-%d'),
    "description" : "pject 1 decription",
    "roles" : [
        {'role_type':'PR', 'role_count':5, 'collab_type':'P', 'budget':5, 'exec_mode':'P'},
        {'role_type':'DJ', 'role_count':2, 'collab_type':'U', 'budget':15, 'exec_mode':'V'},
        {'role_type':'FD', 'role_count':2, 'collab_type':'U', 'budget':15, 'exec_mode':'V'},
        ],
    #"project_status" : "PS",
    "sample_wrk": {
        "text": "this is description of sample work for pject#1",
        "link": "http://medium.com"
    }
}

 
r = requests.post('http://127.0.0.1:8000/app1/projects/', json = data)
#r = requests.post('http://localhost:8000/app1/hello/')
 
print (type(r))
print (r)
print (r.status_code)
print (r.json())

