import json
import requests
import datetime as dt

t1 = dt.datetime.today()
delta = dt.timedelta(days=80)
t2 = t1 + delta
t1 = t1.strftime('%Y-%m-%d')
t2 = t2.strftime('%Y-%m-%d')

#r = requests.get('http://127.0.0.1:8000/app1/projects/filter/?role_types=Photographer,Writer&collab_types=Paid,Unpaid')
#r = requests.get('http://127.0.0.1:8000/app1/projects/filter/?role_types=Photographer,Model&collab_types=Paid&exec_modes=Virtual')

url = 'http://127.0.0.1:8000/app1/projects/filter/?role_types=Photographer,DJ,Model&collab_types=Paid,Unpaid'
#url = f'{url}&completion_date_min={t1}&completion_date_max={t2}'
print(url)

r = requests.get(url)
 
print (type(r))
print (r)
print (r.status_code)
res = r.json()
print(res)
print('--------------------')

for r in res['filters'] :
    print(r, res['filters'][r])
    print()
