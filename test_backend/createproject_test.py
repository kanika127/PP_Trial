import json
import requests
import datetime as dt

data = {
    "username": "Krish",
    "title": "PRADEEP 1 TITLE",
    "medium": "PRADEEP  1 MEDIUM",
    "approx_completion_date" : dt.datetime.today().strftime('%Y-%m-%d'),
    "description" : "PRADEEP 1 .200 DECRIPTION",
    "roles" : [
        {'role_type':'DJ', 'role_count':2, 'collab_type':'U', 'budget':25, 'exec_mode':'V',
            "question_1" : {'prompt':'my q1', 'guidelines':'guide to q2', 'content_type':'I'},
            "question_2" : {'prompt':'my q2', 'guidelines':'guide to q2'},
            "question_3" : {'prompt':'my q2', 'guidelines':'guide to q2'},
        },
        {'role_type':'WR', 'role_count':2, 'collab_type':'U', 'budget':25, 'exec_mode':'V',
            "question_1" : {}, "question_2" : {}, "question_3" : {}},
        {'role_count':5, 'collab_type':'P', 'budget':5, 'exec_mode':'P',
            "question_1" : {}, "question_2" : {}, "question_3" : {}},
        ],
    # "project_status" : "PS",
    "sample_wrk": {
        "text": "THIS IS DESCRIPTION OF SAMPLE WORK FOR PRADEEP 1 #22abcd",
        "link": "http://medium.com"
    },
}

 
r = requests.post('http://127.0.0.1:8000/app1/projects/', json = data)
 
print (type(r))
print (r)
print (r.status_code)
res = r.json()
for key in res :
    print(f'{key} ::: {res[key]}')

