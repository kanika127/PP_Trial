from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status

from django.core.mail import send_mail
from django.http import JsonResponse

from app1.models import Application
from app1.serializers import *

class ApplicationPagination(LimitOffsetPagination):
    default_limit = 15
    max_limit = 15

class ApplicationListCreateAPIView(ListCreateAPIView):
    #queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def post(self, request, *args, **kwargs):
        #serializer = ApplicationSerializer(data=request.data)
        serializer = self.get_serializer(data=request.data)
        print("Received data:", request.data)  # Debugging: Check what data is received
        print("1") ##

        if serializer.is_valid() :
            print('aft validation')
            data = serializer.validated_data
            print('data aft is_valid -->', data)
            application = serializer.save()
        # following added  by nikks ???
        data = request.data ### Nikks added
        print(data)
        # above added  by nikks ???

        self.send_verification_email(data, request)
        return JsonResponse({"message": "Application created and email sent for screening. Please check your messages."})

    def send_verification_email(self, data, request):
        message = "An application is received from " + data['username'] + " for the role of " + data['role'].split('\'')[1] + " in the project " + data['role'].split()[-2] + "."
        print("in ApplicationListCreateAPIView.send_verification_email, message: ", message)
        send_mail(
            'New Application Received',
            # f'Please click on the link to verify your email: {verification_link}',
            # f'An application is received for {message}', #.role}',
            f'{message}', #.role}', ### Nikks updated
            # 'from@example.com',
            # settings.EMAIL_HOST_USER,   
            "kanika127@gmail.com",
            # ("agarwalvandana127@gmail.com",), 
            ["kanika127@gmail.com"],
            fail_silently=False,
        )
        print("email sent")

#class Project_Retrieve_Update_Destroy_View(RetrieveUpdateDestroyAPIView):
    #queryset = Project.objects.all().prefetch_related('roles')
    #serializer_class = ProjectDetailSerializer
    #lookup_field = 'id' # by default looks up for 'pk'

class ApplicationListByOwnerAPIView(ListAPIView):
    serializer_class = ApplicationListSerializer
    pagination_class = ApplicationPagination
