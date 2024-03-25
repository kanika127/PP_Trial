from rest_framework import serializers
from .models import *
 
class SerializerMyClient(serializers.ModelSerializer):
    class Meta :
        model = MyClient
        fields = ['org_name', 'industry', 'address', 'email']


