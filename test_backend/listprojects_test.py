import json
import requests
import datetime as dt

url = 'http://127.0.0.1:8000/app1/projects/'
#url += '?order_by=approx_completion_date'
url += '?order_by=titlee'

while url :
    r = requests.get(url)
     
    print (type(r))
    print (r)
    print (r.status_code)
    r = r.json()
    if not r['previous'] : json.dump(r, open('payload_sz.json', 'w'))
    for k in r :
        if k!='results' :
            print(f'{k} : {r[k]}')
        else :
            print(k)
            for item in r[k] :
                print(item)
    print('******************************')
    url = r['next']
