from rest_framework import serializers
from .models import *
 
class SerializerMyClient(serializers.ModelSerializer):
    class Meta :
        model = MyClient
        fields = ['org_name', 'industry', 'address', 'email']

class ClientSerializer(serializers.ModelSerializer):
    class Meta :
        model = Client
        # fields = '__all__'
        fields = ['email', 'mobile', 'bio', 'sample_work', 'org_name', 'industry', 'password', 'last_login', 'is_superuser', 'username', 'date_joined']

class RoleSerializer(serializers.ModelSerializer):
    class Meta :
        model = Role
        fields = '__all__'
