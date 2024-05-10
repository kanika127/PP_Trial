from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status

from django.core.mail import send_mail
from django.http import JsonResponse

from app1.models import Application
from app1.serializers import *

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
        self.send_verification_email(data, request)
        return JsonResponse({"message": "Application created and email sent for screening. Please check your messages."})

    def send_verification_email(self, data, request):
        print("in ApplicationListCreateAPIView.send_verification_email, data: ", data)
        send_mail(
            'New Application Received',
            # f'Please click on the link to verify your email: {verification_link}',
            f'An application is received for {data}', #.role}',
            # 'from@example.com',
            # settings.EMAIL_HOST_USER,   
            "kanika127@gmail.com",
            ("agarwalvandana127@gmail.com",), 
            fail_silently=False,
        )
        print("email sent")

#class Project_Retrieve_Update_Destroy_View(RetrieveUpdateDestroyAPIView):
    #queryset = Project.objects.all().prefetch_related('roles')
    #serializer_class = ProjectDetailSerializer
    #lookup_field = 'id' # by default looks up for 'pk'
