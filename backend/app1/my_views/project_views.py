from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import NotFound
from rest_framework import serializers

from django.db.models import Q

from app1.models import Project
from app1.serializers import *

class ProjectPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 10

class ProjectListCreateAPIView(ListCreateAPIView):
    queryset = Project.objects.all().prefetch_related('roles') # prefetch_related('roles'):optimizes retrieval of Project instances along with their related Role instances
    pagination_class = ProjectPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProjectListSerializer
        return ProjectSerializer

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

    #def get(self, request, *args, **kwargs):
        #project_id = kwargs.get('id')
        #username = kwargs.get('username')

        ## Check if the project ID and username exist in the Client table
        #if not PassionUser.objects.filter(username=username, projects__id=project_id).exists():
            #raise NotFound("Project not found for the specified username.")

        #return super().get(request, *args, **kwargs)

class ProjectOneSearchView(ListAPIView):
    serializer_class = ProjectListSerializer
    pagination_class = ProjectPagination

    def get_queryset(self):
        search_fields = ('title', 'owner__username') # ('field1', 'field2')  # Add the fields you want to enable search for
        # Split the search term into individual terms
        search_term = self.request.query_params.get('terms', '')
        terms = search_term.split(' ')

        queryset = Project.objects.all()
        #print(queryset)

        # Create a Q object to filter on each term for title, owner__username, medium and role
        title_q = Q()
        username_q = Q()
        medium_q = Q()
        role_q = Q()

        for term in terms:
            title_q |= Q(title__icontains=term)
            username_q |= Q(owner__username__icontains=term)
            medium_q |= Q(medium__icontains=term)

        #role_q |= Q(roles__role_type__iexact=role)

        # Combine all filters 
        from itertools import combinations
        q_objs = ['title_q', 'username_q', 'medium_q', 'role_q']
        combinations_list = []
        for i in range(4, 0, -1) :
            combinations_list += list(combinations(q_objs, i))
        print(combinations_list)
        cmd = ''
        for i, objs in enumerate(combinations_list) :
            print(objs)
            expr = ''
            expr += ' and '.join(objs)
            print(expr)
            if i== 0 :
                cmd = 'if expr :\n'
            else :
                cmd = 'elif expr :\n'
            cmd += '    expr_inner = None\n'
            cmd += f'    expr_inner = " | ".join({objs})\n'
            cmd += '    queryset = queryset.filter(expr_inner)\n'
            cmd += '    print(expr_inner)\n'

        print(cmd)
        #ABCD
        if title_q and username_q and medium_q and role_q :
            queryset = queryset.filter(title_q | username_q | medium_q | role_q)
        # ABC, ABD, ACD, BCD, 
        elif title_q and username_q and medium_q :
            queryset = queryset.filter(title_q | username_q | medium_q)
        elif title_q and username_q and role_q :
            queryset = queryset.filter(title_q | username_q | role_q)
        elif title_q and medium_q and role_q:
            queryset = queryset.filter(title_q | medium_q | role_q)
        elif username_q and medium_q and role_q :
            queryset = queryset.filter(username_q | medium_q | role_q)
        # AB, AC, AD, BC, BD, CD
        elif title_q and username_q :
            queryset = queryset.filter(title_q | username_q)
        elif title_q and medium_q :
            queryset = queryset.filter(title_q | medium_q)
        elif title_q and role_q :
            queryset = queryset.filter(title_q | role_q)
        elif username_q and medium_q :
            queryset = queryset.filter(username_q | medium_q)
        elif username_q and role_q :
            queryset = queryset.filter(username_q | role_q)
        elif medium_q and role_q :
            queryset = queryset.filter(medium_q | role_q)
        # A, B, C, D
        elif title_q:
            queryset = queryset.filter(title_q)
        elif username_q:
            queryset = queryset.filter(username_q)

        print(queryset)
        print(queryset.query)

        return queryset

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
