from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .models import Creator
from .forms import CreatorForm

import datetime

from .models import *

# Create your views here.

from django.http import JsonResponse

@csrf_exempt
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

# def signupClient(request) :
#     user = User.objects.create_user(username=request.data.get('name'), email='user_one@gmail.com', password='iamclient')
#     # user = User.objects.create_user(username='user_one', email='user_one@gmail.com', password='iamclient')
#     return HttpResponse('Client created')

# def signupCreator(request) :
#     user = User.objects.create_user(username='creator1', email='creator@gmail.com', password='iamcreator1')
#     return HttpResponse('Creator created')


### TODO: ASK: I should remove email from user.
class myUser(APIView):
    def __init__(self):
        print("myuser __int__") ##
        self.email = ""
        self.username = ""
        self.password = ""
        self.is_creator = True

    def post(self, request, action):
        print("in myUser post response") ##
        print(action) ##

        if action == "signup":
            self.email = request.data.get('email')
            self.password = request.data.get('password')
            # Check if the username already exists
            try:
                if User.objects.filter(email=self.email).exists():
                    raise ValidationError('Username already exists')    
            except ValidationError as e:
                return JsonResponse({'error': str(e.message)}, status=400)
            user = User.objects.create_user(username=self.email, email=self.email, password=self.password)
            user.save()
            return Response({"message": "User profile created"}, status=status.HTTP_200_OK)
        elif action == "login":
            self.email = request.data.get('email')
            self.password = request.data.get('password')
            print(self.email, self.password) ##
            # Authenticate the user
            user = authenticate(request, username=self.email, password=self.password)
            if user is not None:
                # If credentials are valid, log the user in
                login(request, user)
                return Response({"message": "You're logged in."}, status=status.HTTP_200_OK)
            else:
                print("Invalid login credentials.") ##
                try:
                    if User.objects.filter(email=self.email).exists():
                        raise ValidationError('Incorrect password.')    
                    else:
                        raise ValidationError('Invalid username.')    
                except ValidationError as e:
                    return JsonResponse({'error': str(e.message)}, status=400)
        elif action == "reset_pass":
            self.email = request.data.get('email')
            user = User.objects.get(username=self.email)
            self.password = request.data.get('password')
            user.set_password(self.password)
            print(self.email, self.password)
            user.save()
            return Response({"message": "Your password is updated."}, status=status.HTTP_200_OK)

        elif action == "set_creator":
            self.is_creator = True
            return Response({"message": "Set as creator."}, status=status.HTTP_200_OK)

        elif action == "set_client":
            self.is_creator = False
            return Response({"message": "Set as client."}, status=status.HTTP_200_OK)

        elif action == "add_creator_data":

            return Response({"message": "Creator profile updated."}, status=status.HTTP_200_OK)

### TODO: Check the below
# @login_required
def add_creator_profile(request):
    try:
        creator_profile = request.user.creator
    except Creator.DoesNotExist:
        creator_profile = Creator(user=request.user)

    if request.method == 'POST':
        form = CreatorForm(request.POST, instance=creator_profile)
        if form.is_valid():
            form.save()
            return redirect('profile_updated_successfully')
    else:
        form = CreatorForm(instance=creator_profile)

    return render(request, 'update_creator_profile.html', {'form': form})