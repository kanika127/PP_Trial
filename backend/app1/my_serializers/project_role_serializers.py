from rest_framework import serializers
from django.core.validators import RegexValidator
from django.db.utils import IntegrityError
from app1.models import *
 
class RoleQuestionSerializer(serializers.ModelSerializer):
    class Meta :
        model = RoleQuestion
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    question_1 = RoleQuestionSerializer()
    question_2 = RoleQuestionSerializer()
    question_3 = RoleQuestionSerializer()

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
        fields = ('id', 'title', 'medium', 'owner', 'approx_completion_date', 'roles')

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

        print('data returned by validate --->', data)
        return data

    def create(self, validated_data):
        # Remove the username from validated data and use it to find the BaseUser instance
        if 'project_status' in validated_data :
            validated_data.pop('project_status')
        username = validated_data.pop('username')
        validated_data.pop('owner')
        roles_data = validated_data.pop('roles')
        samplewrk = validated_data.pop('sample_wrk')
        samplewrk = ProjectSampleWorkTable.objects.create(**samplewrk)
        user = BaseUser.objects.get(username=username)  # We know the user exists because of validate
        passion_user = PassionUser.objects.get(username=user)

        # Create the Project instance
        print("BEF PROJ CREATE")
        try :
            project = Project.objects.create(owner=passion_user, sample_wrk=samplewrk, **validated_data)
            print('project created')
            print('======================')
            print()
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'Project with this owner and title already exists.'})

        # print(roles_data)
        for role_data in roles_data :
            role_data.pop('project')
            
            # get question data
            question_1_data = role_data.pop('question_1')
            question_2_data = role_data.pop('question_2')
            question_3_data = role_data.pop('question_3')
            q1 = RoleQuestion.objects.create(**question_1_data)
            q2 = RoleQuestion.objects.create(**question_2_data)
            q3 = RoleQuestion.objects.create(**question_3_data)

            # create role now
            role = Role.objects.create(project=project, question_1=q1, question_2=q2, question_3=q3, **role_data)

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

class Role_FilterProject_Serializer(serializers.ModelSerializer):
    class Meta : 
        model = Role
        fields = ('role_type', 'collab_type', 'exec_mode')

class FilterProjectSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Project
        fields = ['approx_completion_date']

class CreateProjectFilterSerializer(serializers.ModelSerializer) :
    # Filter based on following attributes
    # Role - multi-select ---> role_type in Role
    # Paid/Unpaid/Collaboration - multi-select ---> collab_type in Role
    # Completion Date  - date range ---> approx_completion_date in Project
    # In Person / Virtual - multi-select ---> exec_mode in Role

    project = ProjectSerializer(source='foreign_key_to_project', read_only=True)

    class Meta :
        model = Role
        fields = ('role_type', 'collab_type', 'exec_mode', 'project')

    def to_representation(self, instance):
        # Get the serialized data using the default representation
        data = super().to_representation(instance)
        project_instance = Project.objects.get(pk=instance["project"])  #pk=78)
        project_data = FilterProjectSerializer(project_instance).data  # Serialize ModelA instance separately
        data['project'] = project_data  # Include ModelA data in the serialized representation

        # Group the values of intoch filter field to respective lists
        result = {}
        print('=========================================')
        print(f'{instance=}')
        print(f'{data=}')
        for key, value in data.items():
            if key not in result:
                result[key] = [value]
            else:
                result[key].append(value)

        print(f'{result=}')
        print('=========================================')
        print('=========================================')
        print()
        return result
