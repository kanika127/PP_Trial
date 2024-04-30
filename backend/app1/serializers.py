from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import *
from .my_serializers.project_role_serializers import *
from .my_serializers.application_serializers import *
from .my_serializers.temptesting_serializers import *
 
class UserRegistrationSerializer(serializers.Serializer):
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
