import json
import requests
import datetime as dt

#r = requests.get('http://127.0.0.1:8000/app1/projects/filter/?role_types=Photographer,Writer&collab_types=Paid,Unpaid')
#r = requests.get('http://127.0.0.1:8000/app1/projects/filter/apply/?role_types=Photographer,DJ,Model&collab_types=Paid,Unpaid')

roles = ','.join(['Photographer', 'DJ', 'Model'])  #['Web Designer', 'Photographer', 'DJ', 'Model', 'Writer', 'Instrumentalist'])
url = 'http://127.0.0.1:8000/app1/projects/filter/apply/?role_types='
url += roles

collabs = ','.join(['Paid', 'Unpaid'])
url += '&collab_types='
url += collabs

completion_dates = ','.join(['2024-06-13', '2024-07-04', '2024-07-18', '2024-07-17', '2024-05-31', '2024-06-27'])
url += '&completion_dates='
url += completion_dates

#url += '&order_by=approx_completion_date'
url += '&order_by=title'

print(url)
 
while url :
    r = requests.get(url)
    print (type(r))
    print (r)
    print (r.status_code)
    r = r.json()
    for k in r :
        if k!='results' :
            print(f'{k} : {r[k]}')
        else :
            print(k)
            for item in r[k] :
                print(item)
    print('******************************')
    url = r['next']

