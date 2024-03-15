from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import datetime

from .models import *

# Create your views here.

from django.http import JsonResponse

@csrf_exempt
def hello(request) :
    print('REQ RECVD ....')
    print('******')
    tm = str(datetime.datetime.today())
    resp = {'message' : 'HELLO from DJANGO', 'count':10, 'date' : tm}
    return JsonResponse(resp)

def createClient(request) :
    client = Client(org_name="ORG1", industry='music', address='NYC')
    client.save()
    client = Client(org_name="ORG2", industry='acting', address='SF')
    client.save()
    
    all_clients = {}
    for client in Client.objects.all() :
        all_clients[client.org_name] = client.industry
        print(client)
    return JsonResponse(all_clients)

def createCreator(request) :
    creator = Creator(name='Nikki', mobile='1111111111', address='San Jose', field='music', pronoun='S')
    creator.save()

    creators = {}
    for creator in Creator.objects.all() :
        creators[creator.name] = (creator.mobile, creator.field)
        print(creator)
    return JsonResponse(creators)

def signupClient(request) :
    user = User.objects.create_user(username='user_one', email='user_one@gmail.com', password='iamclient')
    return HttpResponse('Client created')

def signupCreator(request) :
    user = User.objects.create_user(username='creator1', email='creator@gmail.com', password='iamcreator1')
    return HttpResponse('Creator created')
    
