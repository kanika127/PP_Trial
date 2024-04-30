import json
import requests
import datetime as dt

url = 'http://127.0.0.1:8000/app1/projects/detail/7'
r = requests.get(url)
 
print (type(r))
print (r)
print (r.status_code)
r = r.json()
print(r)
