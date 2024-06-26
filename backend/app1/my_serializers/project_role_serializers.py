from rest_framework import serializers
from django.core.validators import RegexValidator
from app1.models import *
 
class RoleSerializer(serializers.ModelSerializer):
    class Meta :
        model = Role
        fields = '__all__'

class ProjectSampleWorkSerializer(serializers.ModelSerializer):
    class Meta :
        model = ProjectSampleWorkTable
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)  # Accept username, but don't include it in the serialized output

    sample_wrk = ProjectSampleWorkSerializer()  # This line specifies that 'sample_wrk' will be handled by ProjectSampleWorkSerializer
    roles = RoleSerializer(many=True)

    class Meta :
        model = Project
        fields = '__all__'
        # depth = 1 
    
    def validate(self, data) :
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
            if role['role_type'] == 'O' and not role.get('other_role_type'):
                raise serializers.ValidationError({'role_type' : "Please provide 'other_role_type' for roles where 'role_type' is 'other'."})

        return data

    def create(self, validated_data):
        # Remove the username from validated data and use it to find the MyUser instance
        username = validated_data.pop('username')
        roles_data = validated_data.pop('roles')
        samplewrk = validated_data.pop('sample_wrk')
        samplewrk = ProjectSampleWorkTable.objects.create(**samplewrk)

        user = BaseUser.objects.get(username=username)  # We know the user exists because of validate_username
        passion_user = PassionUser.objects.get(username=user)

        # Create the Project instance
        project = Project.objects.create(owner=passion_user, sample_wrk=samplewrk, **validated_data)

        for role_data in roles_data :
            Role.objects.create(project=project, **role_data)
        return project

    #def update(self, instance, validated_data):
        #roles_data = validated_data.pop('roles', [])
        ## Update the project fields
        #for attr, value in validated_data.items():
            #setattr(instance, attr, value)
        #instance.save()

        ## Update or create roles
        #for role_data in roles_data:
            #role_id = role_data.get('id', None)
            #if role_id:
                #role = Role.objects.get(id=role_id, project=instance)
                #for key, value in role_data.items():
                    #setattr(role, key, value)
                #role.save()
            #else:
                #Role.objects.create(project=instance, **role_data)

        #return instance
