from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from django.http import JsonResponse

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

class Project_Retrieve_Update_Destroy_View(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all().prefetch_related('roles')
    serializer_class = ProjectDetailSerializer
    lookup_field = 'id' # by default looks up for 'pk'

