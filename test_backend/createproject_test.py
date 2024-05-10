import json
import requests
import datetime as dt

data = {
    "username": "Kanika",
    "title": "Kanika title",
    "medium": "Kanika  medium",
    "approx_completion_date" : dt.datetime.today().strftime('%Y-%m-%d'),
    "description" : "Kanika.100 decription",
    "roles" : [
        {'role_type':'M', 'role_count':2, 'collab_type':'U', 'budget':15, 'exec_mode':'V',
            "question_1" : {'prompt':'my q1', 'guidelines':'guide to q1', 'content_type':'I'},
            "question_2" : {'prompt':'my q2', 'guidelines':'guide to q2'},
            "question_3" : {'prompt':'my q2', 'guidelines':'guide to q2'},
            "question_4" : {'prompt':'my q2', 'guidelines':'guide to q2'},
        },
        {'role_type':'WR', 'role_count':2, 'collab_type':'U', 'budget':15, 'exec_mode':'V',
            "question_1" : {}, "question_2" : {}, "question_3" : {}},
        {'role_count':5, 'collab_type':'P', 'budget':5, 'exec_mode':'P',
            "question_1" : {}, "question_2" : {}, "question_3" : {}},
        ],
    "project_status" : "PS",
    "sample_wrk": {
        "text": "this is description of sample work for Kanika #12abcd",
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

