
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from django.http import JsonResponse

from app1.models import Application
from app1.serializers import *

class ApplicationListCreateAPIView(ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ApplicationSerializer

#class Project_Retrieve_Update_Destroy_View(RetrieveUpdateDestroyAPIView):
    #queryset = Project.objects.all().prefetch_related('roles')
    #serializer_class = ProjectDetailSerializer
    #lookup_field = 'id' # by default looks up for 'pk'

