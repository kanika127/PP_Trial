# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# import datetime

# from app1.models import *
# from app1.serializers import *

# @csrf_exempt
# def hello(request) :
#     print('REQ RECVD ....', request, type(request))
#     print('******')
#     tm = str(datetime.datetime.today())
#     resp = {'message' : 'HELLO from DJANGO', 'count':10, 'date' : tm}
#     return JsonResponse(resp)

# def createCreator(request) :
#     creator = Creator(name='Nikki', mobile='1111111111', address='San Jose', field='music', pronoun='S')
#     creator.save()

#     creators = {}
#     for creator in Creator.objects.all() :
#         creators[creator.name] = (creator.mobile, creator.field)
#         print(creator)
#     return JsonResponse(creators)

# def createClient(request) :
#     email = 'kanika@xx.com'
#     mobile = to_python('+919100041000')
#     client = MyClient(org_name="ORG_2", industry='actor', address='NY2', email=email, mobile=mobile, application_status='O', other_status='We will revert back on your special status')
#     client.full_clean()
#     client.save()
#     print('client SAVED')

#     all_clients = {}
#     for client in MyClient.objects.all() :
#         all_clients[client.org_name] = client.industry
#         print('******', client)
#     ser = SerializerMyClient(client)
#     print('######', ser)
#     return JsonResponse(ser.data) #all_clients)

# def createApplication(request) :
#     role = Role.objects.filter(role_count=10)
#     print(role[0])
#     mobile = to_python('+919100000333')

#     creator = Creator(field=['dance', 'music'], email='kanika@abc.abc', mobile=mobile, sample_work='sample 4', password='pass4', username='user2', pronoun='S', star_rating=4)
#     creator.full_clean()
#     creator.save()

#     application = Application(role=role[0], applicant=creator)
#     application.full_clean()
#     application.save()
#     ret = {'status':'ok'}
#     return JsonResponse(ret)

# def getRoles(request) :
#     ch = DynamicRoleChoices.get_choices()
#     print(ch)
#     roles = {'roles':ch}
#     return JsonResponse(roles)

# def addRole(request) :
#     mobile = to_python('+919100000333')
#     cl = Client(industry=['dance', 'music'], email='guneeti@abc.abc', mobile=mobile, sample_work='sample 4', password='pass4', username='user4', org_name='another4 org')
#     cl.full_clean()
#     cl.save()

#     sample = SampleWrkTbl(text='text4', link='https://www.geek4.com')
#     sample.save()

#     proj = Project(owner=cl, title='proj4', medium='med4', approx_completion_date=datetime.datetime.today(), description='desc134', sample_wrk=sample, project_status='C')
#     proj.full_clean()
#     proj.save()

#     #role = Role(role_count=1, project=proj, budget=5, role_type='O', other_role_type='this is new role type')
#     role = Role(role_count=10, budget=11, project=proj, role_type='O', other_role_type='a new role')
#     role.full_clean()
#     role.save()
#     ser = RoleSerializer(role)
#     return JsonResponse(ser.data)


