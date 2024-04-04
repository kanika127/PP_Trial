from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
# from twilio.rest import Client
from twilio import rest
from twilio.base.exceptions import TwilioRestException
from django.core.mail import send_mail
from django.urls import reverse
from .models import EmailVerificationToken
from django.utils.timezone import now, timedelta
from .serializers import UserRegistrationSerializer
from phonenumber_field.phonenumber import to_python
import random
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
        self.first_name = ""
        self.last_name = ""
        self.username = ""
        self.email = ""
        self.username = ""
        self.password = ""
        self.is_creator = True

    def post(self, request, action):
        print("in PassionViewUser post response") ##
        print(action) ##

        BaseModelUser = get_user_model()
        if action == "signup":
            self.first_name = request.data.get('first_name')
            self.last_name = request.data.get('last_name')
            self.username = request.data.get('username')
            self.email = request.data.get('email')
            self.mobile = request.data.get('mobile')
            self.password = request.data.get('password')
            print('########### SIGNUP ->', self.email, self.password) ##
            # Check if the username already exists
            try:
                # if BaseModelUser.objects.filter(email=self.email).exists():
                if BaseModelUser.objects.filter(username=self.username).exists():
                    raise ValidationError('Username already exists')    
            except ValidationError as e:
                return JsonResponse({'error': str(e.message)}, status=400)
            user = BaseModelUser.objects.create_user(username=self.username, email=self.email, password=self.password)
            # user = BaseModelUser.objects.create_user(email=self.email, password=self.password)
            # user = User(username=self.email, email=self.email, password=self.password) -> check again
            try:
                user.full_clean()
                print("cleaned up ")##
            except ValidationError as e:
                # Handle validation errors
                error_message = e.message_dict.get('email', ['An error occurred. Please try again.'])[0]
                return JsonResponse({'error': error_message}, status=400)
            user.save()
            print("saved user")##
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
            # user = PassionViewUser.objects.get(username=self.email) ## mum
            user = BaseModelUser.objects.get(username=self.email) ## nix
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


class UserRegistrationView(APIView):
    def post(self, request, action):
        print("in UserRegistrationView post")
        print(request.data)
        if action == "check_username":
            print(action) ##
            # data = json.loads(request.body)
            data = request.data
            username = data['username']
            is_available = not User.objects.filter(username=username).exists()
            return JsonResponse({'isAvailable': is_available})
        else:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                print("serializer is valid") ###
                data = serializer.validated_data
                # Store the user data somewhere, maybe in session or a temporary store
                # Since we're focusing on email verification, we'll skip directly to sending the email

                # email_exists, email_error = self.does_email_exist(data)
                email_exists, email_error = self.does_email_exist(data["email"])
                mobile_exists, mobile_error = self.does_mobile_exist(data["mobile"])
                username_exists, username_error = self.does_username_exist(data["username"])
                e = None
                if email_exists:
                    e = email_error
                if mobile_exists:
                    e = mobile_error
                if username_exists:
                    e = username_error
                if e is not None:
                    return JsonResponse({'error': str(e.message)}, status=400)

                self.send_verification_email(data, request)
                return Response({"message": "Verification code sent. Please check your messages."})
                # self.send_verification_email(data, request)
                # return Response({"message": "Verification email sent. Please check your inbox."})
            password_errors = serializer.errors.get('password', [])
            mobile_errors = serializer.errors.get('mobile', [])
            print("serializer is invalid cz ", mobile_errors) ###
            return Response({"error": password_errors}, status=400)
    
    def verify_phone_number(request):
        mobile = request.POST.get('mobile')
        code = request.POST.get('code')
        try:
            verification = PhoneVerification.objects.get(mobile=mobile)
            if verification.is_code_valid(code):
                return JsonResponse({"success": True, "message": "Phone number verified."})
            else:
                return JsonResponse({"success": False, "message": "Invalid or expired code."})
        except PhoneVerification.DoesNotExist:
            return JsonResponse({"success": False, "message": "Verification record not found."})

    def generate_verification_code(self, mobile):
        code = random.randint(100000, 999999)  # Generate a 6-digit code
        # expiration = datetime.now() + timedelta(minutes=10)  # Code expires in 10 minutes
        # Store code and expiration in your database
        PhoneVerification.objects.update_or_create(
            mobile=mobile,
            defaults={'code': code}
            # defaults={'code': code, 'expires_at': expiration}
        )
        return code
    
    def send_verification_code_to_mobile(self, mobile_number):
        mobile_number = "+1" + mobile_number
        print("mobile: ", mobile_number) ###
        code = self.generate_verification_code(mobile_number)
        client = rest.Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        # try:
        message = client.messages.create(
            body=f"Your verification code is: {code}",
            messaging_service_sid=settings.TWILIO_MSG_SERVICE_SID,
            # from_=settings.TWILIO_PHONE_NUMBER,
            to=settings.TWILIO_PHONE_NUMBER
            # to="+17033888636"
            # to=mobile_number
        )
        print(message.sid)  # For logging purposes


    def send_verification_email(self, data, request):
        print("in UserRegistrationView.send_verification_email, data: ", data)
        token = EmailVerificationToken.objects.create(
            email=data["email"],
            expires_at=now() + timedelta(hours=1),  # Token expires in 1 hour
            user_data=data
        )
        verification_link = request.build_absolute_uri(
            reverse('email-verify') + f'?token={token.token}'
        )
        send_mail(
            'Verify your email',
            f'Please click on the link to verify your email: {verification_link}',
            # 'from@example.com',
            settings.EMAIL_HOST_USER,   
            [data["email"]],
            fail_silently=False,
        )

    def does_email_exist(self, email):
        BaseModelUser = get_user_model()
        try:
            if BaseModelUser.objects.filter(email=email).exists(): ## TODO: filter based on username
                raise ValidationError('Email already exists')    
        except ValidationError as e:
            return (True, e)
        return (False, None)

    def does_mobile_exist(self, mobile):
        BaseModelUser = get_user_model()
        try:
            if BaseModelUser.objects.filter(mobile=mobile).exists(): ## TODO: filter based on username
                raise ValidationError('Mobile already exists')    
        except ValidationError as e:
            return (True, e)
        return (False, None)

    def does_username_exist(self, username):
        BaseModelUser = get_user_model()
        try:
            if BaseModelUser.objects.filter(username=username).exists(): ## TODO: filter based on username
                raise ValidationError('Username already exists')    
        except ValidationError as e:
            return (True, e)
        return (False, None)

class EmailVerifyView(APIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            token_obj = EmailVerificationToken.objects.get(token=token, expires_at__gt=now())
            # Here you would create the User object using the stored details
            # Since we're simulating, let's assume we retrieve them like this
            # user_data = retrieve_user_data_somehow()
            print('########### Register') ##
            user_data = token_obj.user_data
            # user_data = token_obj.user_data
            print("user data in email verify view: ", user_data) ###
            # BaseModelUser = get_user_model()
            # user = User.objects.create_user(
            # user = BaseModelUser.objects.create_user(
            # baseuser = BaseModelUser.objects.create_user(
            #     username=user_data["username"],
            #     email=token_obj.email,
            #     mobile=user_data["mobile"],
            #     password=user_data["password"],
            #     first_name=user_data["first_name"],
            #     last_name=user_data["last_name"]
            # )
            # passionuser = PassionUser.objects.create_user(
            # passion_user = PassionUser(
            #     # baseuser_ptr_id=baseuser.id, 
            #     username=user_data["username"],
            #     email=token_obj.email,
            #     mobile=user_data["mobile"],
            #     password=user_data["password"],
            #     first_name=user_data["first_name"],
            #     last_name=user_data["last_name"]
            # )
            # passion_user.set_password(user_data["password"])  # Setting password
            # passion_user.save() 
            # print("role: ", user_data["role"]) ###
            if user_data["role"] == "Creator":
                print("role: creator") ###
                # Creator.objects.create_user(
                creator = Creator(
                    username=user_data["username"],
                    email=token_obj.email,
                    mobile=user_data["mobile"],
                    password=user_data["password"],
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"]
                ) 
                creator.set_password(user_data["password"])  # Setting password
                creator.save() 
            elif user_data["role"] == "Client":
                client = Client.objects.create_user(
                    username=user_data["username"],
                    email=token_obj.email,
                    mobile=user_data["mobile"],
                    # password=user_data["password"],
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"]
                )
                client.set_password(user_data["password"])  # Setting password
                client.save() 
            token_obj.delete()
            return Response({"message": "Email verified successfully. Account created."})
        except EmailVerificationToken.DoesNotExist:
            return Response({"message": "Invalid or expired token."}, status=400)

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
