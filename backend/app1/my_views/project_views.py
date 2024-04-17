from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from django.http import JsonResponse

from app1.models import Project
from app1.serializers import ProjectSerializer

class ProjectListCreateAPIView(ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
#
#class MyModelRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    #queryset = MyModel.objects.all()
    #serializer_class = MyModelSerializer

#class ProjectCreate(CreateAPIView) :

