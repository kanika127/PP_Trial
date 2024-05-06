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

class ProjectSearchView(ListAPIView):
    serializer_class = ProjectListSerializer
    pagination_class = ProjectPagination

    def get_queryset(self):
        queryset = Project.objects.all()
        print(queryset)
        title = self.request.query_params.get('title', None)
        medium = self.request.query_params.get('medium', None)
        owner_username = self.request.query_params.get('owner', None)
        role = self.request.query_params.get('role', None)

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
