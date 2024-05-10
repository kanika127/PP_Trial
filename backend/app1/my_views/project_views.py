from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import NotFound
from rest_framework import serializers
from rest_framework import status

from django.db.models import Q
from django.http import JsonResponse

from app1.models import Project, ROLE_CHOICES
from app1.serializers import *

# class ProjectCreateView(CreateAPIView):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
    
#class ProjectCreateAPIView(CreateAPIView):
    #queryset = Project.objects.all()
    #serializer_class = ProjectSerializer
    # permission_classes = [IsAuthenticated] ### Temporarily commented

    #def __init__(self):
        #print ("in Project create view")

    #def post(self, request, *args, **kwargs):
        #print("Received data:", request.data)  # Debugging: Check what data is received
        #serializer = self.get_serializer(data=request.data)
        ##print("1") ##
        ## # if serializer.is_valid(raise_exception=True):
        ##     # print("2") ##
        ## else:
        ##     print("invalid serializer")
        ##     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        ## self.perform_create(serializer)
        ## print("3") ##
        ## headers = self.get_success_headers(serializer.data)
        ## print("4") ##
        ## return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        #return JsonResponse({"message": "Project created."}, status=status.HTTP_200_OK)

class ProjectPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 10

class ProjectListCreateAPIView(ListCreateAPIView):
    queryset = Project.objects.all().prefetch_related('roles') # prefetch_related('roles'):optimizes retrieval of Project instances along with their related Role instances
    pagination_class = ProjectPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            ser_class =  ProjectListSerializer
        else :
            ser_class = ProjectSerializer
        return ser_class

class ProjectListByOwnerAPIView(ListAPIView):
    serializer_class = ProjectListSerializer
    pagination_class = ProjectPagination

    def get_queryset(self):
        username = self.kwargs['username']  # Assuming the URL pattern includes 'owner_id'
        if not PassionUser.objects.filter(username=username).exists():
            print('NO SUCH USER')
            #raise NotFound("No such user")
        return Project.objects.filter(owner__username=username).prefetch_related('roles')

# project details by owner
class ProjectOwnerView(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all().prefetch_related('roles')
    serializer_class = ProjectDetailOwnerSerializer
    lookup_field = 'id' # by default looks up for 'pk'

# project details by applicant
class ProjectApplicantView(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all().prefetch_related('roles')
    serializer_class = ProjectDetailApplicantSerializer
    lookup_field = 'id' # by default looks up for 'pk'

class ProjectOneSearchView(ListAPIView):
    serializer_class = ProjectListSerializer
    pagination_class = ProjectPagination

    def get_queryset(self):
        search_fields = ('title', 'owner__username') # ('field1', 'field2')  # Add the fields you want to enable search for
        # Split the search term into individual terms
        search_term = self.request.query_params.get('terms', '')
        terms = search_term.split(' ')

        queryset = Project.objects.all()

        # Create a Q object to filter on each term for title, owner__username, medium and role
        title_q = Q()
        username_q = Q()
        medium_q = Q()
        role_q = Q()
        for term in terms:
            title_q |= Q(title__icontains=term)
            username_q |= Q(owner__username__icontains=term)
            medium_q |= Q(medium__icontains=term)
            for ch1, ch2 in ROLE_CHOICES :
                if ch2.upper() == term.upper() : # introduce tokenizer here
                    role_q |= Q(roles__role_type__iexact=ch1)
                    break
            

        # Combine all filters 
        from itertools import combinations
        from functools import reduce
        q_objs = [title_q, username_q, medium_q, role_q]
        combinations_list = []
        for i in range(len(q_objs)+1, 0, -1) :
            combinations_list += list(combinations(q_objs, i))

        for combination in combinations_list :
            if all(combination) :
                combined_q = reduce(lambda x, y: x | y, combination)
                queryset = queryset.filter(combined_q).distinct()
                break
        return queryset

        ####
        # Following huge code has been replaced by the above scalable code section
        # This must be removed after the above scalable section has been well tested
        ####
        #queryset = Project.objects.all()
        #ABCD
        #if title_q and username_q and medium_q and role_q :
            #print('ABCD')
            #queryset = queryset.filter(title_q | username_q | medium_q | role_q)
        # ABC, ABD, ACD, BCD, 
        #elif title_q and username_q and medium_q :
            #print('ABC')
            #queryset = queryset.filter(title_q | username_q | medium_q)
        #elif title_q and username_q and role_q :
            #print('ABD')
            #queryset = queryset.filter(title_q | username_q | role_q)
        #elif title_q and medium_q and role_q:
            #print('ACD')
            #queryset = queryset.filter(title_q | medium_q | role_q)
        #elif username_q and medium_q and role_q :
            #print('BCD')
            #queryset = queryset.filter(username_q | medium_q | role_q)
        # AB, AC, AD, BC, BD, CD
        #elif title_q and username_q :
            #print('AB')
            #queryset = queryset.filter(title_q | username_q)
        #elif title_q and medium_q :
            #print('AC')
            #queryset = queryset.filter(title_q | medium_q)
        #elif title_q and role_q :
            #print('AD')
            #queryset = queryset.filter(title_q | role_q)
        #elif username_q and medium_q :
            #print('BC')
            #queryset = queryset.filter(username_q | medium_q)
        #elif username_q and role_q :
            #print('BD')
            #queryset = queryset.filter(username_q | role_q)
        #elif medium_q and role_q :
            #print('CD')
            #queryset = queryset.filter(medium_q | role_q)
        # A, B, C, D
        #elif title_q:
            #print('A')
            #queryset = queryset.filter(title_q)
        #elif username_q:
            #print('B')
            #queryset = queryset.filter(username_q)
        #elif medium_q:
            #print('C')
            #queryset = queryset.filter(medium_q)
        #elif role_q:
            #print('D')
            #queryset = queryset.filter(role_q)

        #print(queryset.query)
        #print('==========================================')
        #print()
        #return queryset

# Following SEARCH function assumes that there are 4 separate search bars (one for each category
# This assumes that api could be invoked as :-
#       http://127.0.0.1:8000/app1/projects/search/?owner=kanika&role=dj
#       http://127.0.0.1:8000/app1/projects/search/?owner=kanika&title=p
# This is not used presently
# Can be removed later if not required
class ProjectMultiSearchView(ListAPIView):
    serializer_class = ProjectListSerializer
    pagination_class = ProjectPagination

    def get_queryset(self):
        queryset = Project.objects.all()
        print(queryset)
        title = self.request.query_params.get('title', '')
        medium = self.request.query_params.get('medium', '')
        owner_username = self.request.query_params.get('owner', '')
        role = self.request.query_params.get('role', '')

        title_q = Q()
        medium_q = Q()
        username_q = Q()
        role_q = Q()
        if title :
            title_q |= Q(title__icontains=title)
        if medium :
            medium_q |= Q(medium__icontains=medium)
        if owner_username :
            username_q |= Q(owner__username__icontains=owner_username)
        if role :
            role_q |= Q(roles__role_type__iexact=role)

        queryset = queryset.filter(title_q & medium_q & username_q & role_q)
        print(queryset)
        print(queryset.query)

        return queryset
