from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from phonenumber_field.phonenumber import to_python

import datetime

from .models import *
from .forms import CreatorForm, PassionUserProfileForm
from .serializers import *

# Create your views here.

from django.http import JsonResponse

@csrf_exempt
@csrf_exempt
def hello(request) :
    print('REQ RECVD ....', request, type(request))
    print('******')
    tm = str(datetime.datetime.today())
    resp = {'message' : 'HELLO from DJANGO', 'count':10, 'date' : tm}
    return JsonResponse(resp)

def createClient(request) :
    email = 'kanika@xx.com'
    mobile = to_python('+919100041000')
    client = MyClient(org_name="ORG_2", industry='actor', address='NY2', email=email, mobile=mobile, application_status='O', other_status='We will revert back on your special status') 
    client.full_clean()
    client.save()
    print('client SAVED')

    all_clients = {}
    for client in MyClient.objects.all() :
        all_clients[client.org_name] = client.industry
        print('******', client)
    ser = SerializerMyClient(client)
    print('######', ser)
    return JsonResponse(ser.data) #all_clients)

def createApplication(request) :
    role = Role.objects.filter(role_count=10)
    print(role[0])
    mobile = to_python('+919100000333')

    creator = Creator(field=['dance', 'music'], email='kanika@abc.abc', mobile=mobile, sample_work='sample 4', password='pass4', username='user2', pronoun='S', star_rating=4)
    creator.full_clean()
    creator.save()

    application = Application(role=role[0], applicant=creator)
    application.full_clean()
    application.save()
    ret = {'status':'ok'}
    return JsonResponse(ret)

def getRoles(request) :
    ch = DynamicRoleChoices.get_choices()
    print(ch)
    roles = {'roles':ch}
    return JsonResponse(roles)

def addRole(request) :
    mobile = to_python('+919100000333')
    cl = Client(industry=['dance', 'music'], email='guneeti@abc.abc', mobile=mobile, sample_work='sample 4', password='pass4', username='user4', org_name='another4 org')
    cl.full_clean()
    cl.save()

    sample = SampleWrkTbl(text='text4', link='https://www.geek4.com')
    sample.save()

    proj = Project(owner=cl, title='proj4', medium='med4', approx_completion_date=datetime.datetime.today(), description='desc134', sample_wrk=sample, project_status='C')
    proj.full_clean()
    proj.save()

    #role = Role(role_count=1, project=proj, budget=5, role_type='O', other_role_type='this is new role type')
    role = Role(role_count=10, budget=11, project=proj, role_type='O', other_role_type='a new role')
    role.full_clean()
    role.save()
    ser = RoleSerializer(role)
    return JsonResponse(ser.data)

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
class PassionViewUser(APIView):
    def __init__(self):
        print("PassionViewUser __int__") ##
        self.email = ""
        self.username = ""
        self.password = ""
        self.is_creator = True

    def post(self, request, action):
        print("in PassionViewUser post response") ##
        print(action) ##

        PassionModelUser = get_user_model()
        if action == "signup":
            self.email = request.data.get('email')
            self.password = request.data.get('password')
            print('########### SIGNUP ->', self.email, self.password) ##
            # Check if the username already exists
            try:
                if PassionModelUser.objects.filter(email=self.email).exists():
                    raise ValidationError('Username already exists')    
            except ValidationError as e:
                return JsonResponse({'error': str(e.message)}, status=400)
            user = PassionModelUser.objects.create_user(email=self.email, password=self.password)
            # user = User(username=self.email, email=self.email, password=self.password) -> check again
            try:
                user.full_clean()
                print("cleaned up ")##
            except ValidationError as e:
                # Handle validation errors
                error_message = e.message_dict.get('email', ['An error occurred. Please try again.'])[0]
                return JsonResponse({'error': error_message}, status=400)
            user.save()
            print("saved ")##
            print(user)
            return Response({"message": "User profile created"}, status=status.HTTP_200_OK)

        elif action == "login":
            self.email = request.data.get('email')
            self.password = request.data.get('password')
            print('########### LOGIN ->', self.email, self.password) ##
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
            user = PassionViewUser.objects.get(username=self.email)
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
