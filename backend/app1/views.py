from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse

def hello(request) :
    print('REQ RECVD')
    return JsonResponse({'message': 'Hello from Django!'})


