
from rest_framework import serializers
from django.core.validators import RegexValidator
from app1.models import *
 
class ApplicationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)  # Accept username, but don't include it in the serialized output

    class Meta :
        model = Application
        fields = '__all__'
    
    def validate(self, data) :
        required_fields = ['role', 'username']
        
        #missing_fields = [field for field in required_fields if field not in data]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise serializers.ValidationError({field: "This field is required." for field in missing_fields})

        # Check if the username exists in the User model
        if 'username' in data and not BaseUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username' : "This username does not exist."})
        return data

    def create(self, validated_data):
        # Remove the username from validated data and use it to find the Creator instance
        username = validated_data.pop('username')
        validated_data.pop('applicant')
        validated_data.pop('application_status')
        creator = Creator.objects.get(username=username)  # We know the user exists because of validate

        # Create the Application instance
        application = Application.objects.create(applicant=creator, **validated_data)
        return application

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
