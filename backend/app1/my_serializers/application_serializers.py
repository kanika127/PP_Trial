from rest_framework import serializers
from django.core.validators import RegexValidator
from app1.models import *

class ApplicationQuestionSerializer(serializers.ModelSerializer) :
    class Meta :
        model = ApplicationQuestion
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)  # Accept username, but don't include it in the serialized output
    ques_1_content = ApplicationQuestionSerializer()
    ques_2_content = ApplicationQuestionSerializer()
    ques_3_content = ApplicationQuestionSerializer()

    class Meta :
        model = Application
        fields = '__all__'

    def validate(self, data) :
        required_fields = ['role', 'username']

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
        validated_data.pop('application_status') # popped : because application must always be created with default status 'Pending' 
        q1_data = validated_data.pop('ques_1_content')
        q2_data = validated_data.pop('ques_2_content')
        q3_data = validated_data.pop('ques_3_content')
        creator = Creator.objects.get(username=username)  # We know the user exists because of validate
        print("in create application")

        # Create the ApplicationQuestions instances
        print("before creating application questions")
        q1 = ApplicationQuestion.objects.create(**q1_data)
        q2 = ApplicationQuestion.objects.create(**q2_data)
        q3 = ApplicationQuestion.objects.create(**q3_data)

        # Create Application instance
        print("before creating application")
        application = Application.objects.create(applicant=creator, ques_1_content=q1, ques_2_content=q2, ques_3_content=q3, **validated_data)
        print("after creating application", application)

        return application
    
    def withdraw(self, application_id):
        ## TODO: remove application entry
        try:
            application = Application.objects.get(pk=application_id)
            application.delete()
            return JsonResponse({'message': 'Application deleted successfully'}, status=204)
        except Application.DoesNotExist:
            return JsonResponse({'error': 'Application not found'}, status=404)

        return

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

class ApplicationListSerializer(serializers.ModelSerializer):
    # role = Role_ListProject_Serializer(many=False, read_only=True)
    # applicant = Owner_ListProject_Serializer(many=False, read_only=True) 
    class Meta : 
        model = Role
        fields = [field.name for field in model._meta.fields if field.name!='applicant']
