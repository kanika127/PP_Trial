from rest_framework import serializers
from django.core.validators import RegexValidator
from app1.models import *
 
class RoleSerializer(serializers.ModelSerializer):
    class Meta :
        model = Role
        fields = '__all__'

class Role_ListProject_Serializer(serializers.ModelSerializer):
    class Meta : 
        model = Role
        fields = ('role_type', 'collab_type')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.role_type == 'O':
            data['other_role_type'] = instance.other_role_type
        return data

class Role_ApplicationSerializer(serializers.ModelSerializer):
    class Meta :
        model = Application
        fields = ('application_status',)

class Role_ProjectDetailOwner_Serializer(serializers.ModelSerializer):
    applications = Role_ApplicationSerializer(many=True, read_only=True)
    class Meta : 
        model = Role
        fields = [field.name for field in model._meta.fields if field.name!='project'] + ['applications']
        #exclude = ('project', )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.role_type != 'O':
            data.pop('other_role_type', None)
        return data

class Role_ProjectDetailApplicant_Serializer(serializers.ModelSerializer):
    class Meta : 
        model = Role
        exclude = ('project',) #, 'status_newmatch')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.role_type != 'O':
            data.pop('other_role_type', None)
        return data

class Owner_ListProject_Serializer(serializers.ModelSerializer):
    class Meta :
        model = PassionUser
        fields = ('username', 'profile_picture')

class SampleWork_ProjectDetail_Serializer(serializers.ModelSerializer):
    class Meta :
        model = ProjectSampleWorkTable
        fields = ('text', 'link')

class ProjectSampleWorkSerializer(serializers.ModelSerializer):
    class Meta :
        model = ProjectSampleWorkTable
        fields = '__all__'

class ProjectListSerializer(serializers.ModelSerializer):
    roles = Role_ListProject_Serializer(many=True, read_only=True)
    owner = Owner_ListProject_Serializer(many=False, read_only=True) 

    class Meta:
        model = Project
        # fields = ('id', 'title', 'medium', 'owner', 'approx_completion_date', 'roles')
        fields = ('id', 'title', 'medium', 'approx_completion_date', 'roles') ###TODO: check if custon field can be sent from here

class ProjectDetailOwnerSerializer(serializers.ModelSerializer):
    roles = Role_ProjectDetailOwner_Serializer(many=True, read_only=True)
    owner = Owner_ListProject_Serializer(read_only=True)
    sample_wrk = SampleWork_ProjectDetail_Serializer(read_only=True)
    class Meta :
        model = Project
        fields = '__all__'

class ProjectDetailApplicantSerializer(serializers.ModelSerializer):
    roles = Role_ProjectDetailApplicant_Serializer(many=True, read_only=True)
    owner = Owner_ListProject_Serializer(read_only=True)
    sample_wrk = SampleWork_ProjectDetail_Serializer(read_only=True)
    class Meta :
        model = Project
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)  # Accept username, but don't include it in the serialized output

    sample_wrk = ProjectSampleWorkSerializer()  # This line specifies that 'sample_wrk' will be handled by ProjectSampleWorkSerializer
    roles = RoleSerializer(many=True)

    class Meta :
        model = Project
        fields = '__all__'
        # depth = 1 
    
    def __init__(self):
        print("init ProjectSerializer")

    def validate(self, data) :
        print(data)
        print("in validate projetc serializer ---> 1") ####
        # Retrieve all field names from the model
        model_fields = [field.name for field in self.Meta.model._meta.fields if not field.auto_created]

        # Optionally, filter out fields you do not need to validate
        required_fields = [field for field in model_fields if field not in ['id', 'owner']]
        
        # Check each field for presence in the data
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise serializers.ValidationError({field: "This field is required." for field in missing_fields})

        # Check if the username exists in the User model
        if 'username' in data and not BaseUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username' : "This username does not exist."})

        roles_data = data.get('roles')
        for role in roles_data :
            # if role['role_count'] < 1 or role['role_count'] > 10: 
            #     print("://")
            #     raise serializers.ValidationError({'role_count' : "'role_count' should be between 1 and 10 inclusive."})
            if role['role_type'] == 'O' and not role.get('other_role_type'):
                raise serializers.ValidationError({'role_type' : "Please provide 'other_role_type' for roles where 'role_type' is 'other'."})

        print('data returned by validate --->', data)
        return data

    def create(self, validated_data):
        # Remove the username from validated data and use it to find the BaseUser instance
        print('create project func')
        username = validated_data.pop('username')
        validated_data.pop('owner')
        roles_data = validated_data.pop('roles')
        samplewrk = validated_data.pop('sample_wrk')
        samplewrk = ProjectSampleWorkTable.objects.create(**samplewrk)
        print('create func ---> 1')

        user = BaseUser.objects.get(username=username)  # We know the user exists because of validate
        passion_user = PassionUser.objects.get(username=user)
        print('create func ---> 2')

        # Create the Project instance
        project = Project.objects.create(owner=passion_user, sample_wrk=samplewrk, **validated_data)
        print('create func ---> 3')

        # print(roles_data)
        for role_data in roles_data :
            role_data.pop('project')
            Role.objects.create(project=project, **role_data)
            print('create func ---> 4')
        print('project created --->', project)
        return project
    
    def update(self, instance, validated_data):
        print("instance: ", instance)
        return instance
        # instance.title = validated_data.get('title', instance.title)
        # instance.medium = validated_data.get('medium', instance.medium)
        # instance.approx_completion_date = validated_data.get('approx_completion_date', instance.approx_completion_date)
        # instance.description = validated_data.get('description', instance.description)
        # instance.sample_wrk = validated_data.get('sample_wrk', instance.sample_wrk)
        # instance.project_status = validated_data.get('project_status', instance.project_status)
        # instance.save()
        # return instance

        print("0")
        roles_data = validated_data.pop('roles', [])
        # Update the project fields
        print("1")
         
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        print("2")

        ## Update or create roles
        for role_data in roles_data:
            role_id = role_data.get('id', None)
            if role_id:
                role = Role.objects.get(id=role_id, project=instance)
                for key, value in role_data.items():
                    setattr(role, key, value)
                role.save()
            else:
                Role.objects.create(project=instance, **role_data)
            print("3")

        instance.save()
        return instance
