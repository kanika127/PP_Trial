import json
import requests
import datetime as dt

# 85 role-questions
# 35 roles
# 15 projects

data = {
        'project_id' : 99,
        'username' : 'Kanika',
        }

url = 'http://127.0.0.1:8000/app1/projects/delete/'
r = requests.delete(url, params=data)
 
print (type(r))
print (r, type(r))
print ('delete status --->', r.status_code)

if r.status_code==404 :
    print(r.json())
