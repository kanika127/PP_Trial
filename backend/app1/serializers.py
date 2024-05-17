from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import *
from .my_serializers.project_role_serializers import *
from .my_serializers.application_serializers import *
 
class CreatorRegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, validators=[
        RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            message=("Password must contain at least one uppercase letter, "
                     "one lowercase letter, one digit, and one special character and must be atleast 8 characters long.")
        )
    ])
    mobile = serializers.CharField(validators=[
        RegexValidator(
            # regex=r'^\+?1?\d{9,15}$',
            # message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            # regex=r'^\+?1?\d{9,10}$',
            regex=r'^\d{9,10}$',
            # regex=r'^\d[1-9]\d{9,9}$',
            message="Phone number must be entered in the format: '9876543210'. Up to 10 digits allowed."
        )
    ])
    email = serializers.EmailField()
    role = serializers.CharField()
    
class ClientRegistrationSerializer(serializers.Serializer):
    organization_name = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, validators=[
        RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            message=("Password must contain at least one uppercase letter, "
                     "one lowercase letter, one digit, and one special character and must be atleast 8 characters long.")
        )
    ])
    mobile = serializers.CharField(validators=[
        RegexValidator(
            # regex=r'^\+?1?\d{9,15}$',
            # message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            # regex=r'^\+?1?\d{9,10}$',
            regex=r'^\d{9,10}$',
            # regex=r'^\d[1-9]\d{9,9}$',
            message="Phone number must be entered in the format: '9876543210'. Up to 10 digits allowed."
        )
    ])
    email = serializers.EmailField()
    role = serializers.CharField()

'''
### check below if required
class ProjectSampleWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSampleWorkTable
        fields = ['text', 'link']

class ProjectSerializer(serializers.ModelSerializer):
    sample_works = ProjectSampleWorkSerializer(many=True, required=False)
    
    class Meta:
        model = Project
        fields = '__all__'
        # exclude = ('sample_wrk',)

    def create(self, validated_data):
        sample_works_data = validated_data.pop('sample_works', [])
        project = Project.objects.create(**validated_data)
        for sample_work_data in sample_works_data:
            ProjectSampleWorkTable.objects.create(project=project, **sample_work_data)
        return project
    

class RoleSerializer(serializers.ModelSerializer):
    # project = ProjectSerializer()
    project = ProjectSerializer(read_only=True)
    
    class Meta:
        model = Role
        fields = ['role_type', 'other_role_type', 'collab_type', 'budget', 'exec_mode', 'project']
'''
