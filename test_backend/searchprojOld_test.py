import json
import requests
import datetime as dt

owner = input('Enter owner/(press enter for None) :: ').replace(' ', '%20').replace('#', '%23')
medium = input('Enter medium/(press enter for None) :: ').replace(' ', '%20').replace('#', '%23')
title = input('Enter title/(press enter for None) :: ').replace(' ', '%20').replace('#', '%23')
role = input('Enter role/(press enter for None) :: ')

url = 'http://127.0.0.1:8000/app1/projects/search/?'
if owner : url += f'owner={owner}&'
if title : url += f'title={title}&'
if medium : url += f'medium={medium}&'
if role : url += f'role={role}&'
print(url)

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
