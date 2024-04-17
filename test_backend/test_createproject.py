import json
import requests
import datetime as dt

data = {
    "username": "user4",
    "title": "proj#3 title",
    "medium": "proj#3 medium",
    "approx_completion_date" : dt.datetime.today().strftime('%Y-%m-%d'),
    "description" : "project three decription",
    "roles" : [
        {'role_type':'O', 'other_role_type' : 'Graphic Artist', 'role_count':2, 'budget':10}, #'exec_mode':'P'},
        {'role_type':'D', 'role_count':5, 'collab_type':'P', 'budget':5, 'exec_mode':'P'},
        {'role_type':'DJ', 'role_count':2, 'collab_type':'U', 'budget':15, 'exec_mode':'V'},
        {'role_type':'M', 'role_count':20, 'collab_type':'C', 'budget':13, 'exec_mode':'P'},
        ],
    "project_status" : "P",
    "sample_wrk": {
        "text": "this is description of sample work for project#3",
        "link": "http://google.com"
    }
}

 
r = requests.post('http://127.0.0.1:8000/app1/add_project/', json = data)
#r = requests.post('http://localhost:8000/app1/hello/')
 
print (type(r))
print (r)
print (r.status_code)
print (r.json())

