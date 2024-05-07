from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from django.http import JsonResponse

from app1.models import Project
from app1.serializers import *

# class ProjectCreateView(CreateAPIView):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
    
class ProjectCreateAPIView(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # permission_classes = [IsAuthenticated] ### Temporarily commented

    def __init__(self):
        print ("in Project create view")

    def post(self, request, *args, **kwargs):
        print("Received data:", request.data)  # Debugging: Check what data is received
        serializer = self.get_serializer(data=request.data)
        print("1") ##
        # # if serializer.is_valid(raise_exception=True):
        #     # print("2") ##
        # else:
        #     print("invalid serializer")
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # self.perform_create(serializer)
        # print("3") ##
        # headers = self.get_success_headers(serializer.data)
        # print("4") ##
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return JsonResponse({"message": "Project created."}, status=status.HTTP_200_OK)

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

