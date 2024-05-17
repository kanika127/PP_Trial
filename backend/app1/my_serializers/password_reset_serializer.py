from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from rest_framework import status
# from .models import *

class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, validators=[
        RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            message=("Password must contain at least one uppercase letter, "
                     "one lowercase letter, one digit, and one special character and must be atleast 8 characters long.")
        )
    ])

    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        print("hola")
        print("serializer init data", data)
        self.new_password = data.get('new_password')
        # self.validate(data)
        return

    # def validate_password(self, data):
    # def validate_newpassword(self, data):
    def validate(self, data):
        # Validate password using Django's built-in validators
        print("yo")
        print(data) ###
        self.username = data.get('username')
        curr_password = data.get('curr_password')
        self.new_password = data.get('new_password')
        BaseModelUser = get_user_model()
        try:
            self.user = BaseModelUser.objects.get(username=self.username)
        except User.DoesNotExist:
            print("user not present") ###
            raise serializers.ValidationError("user not present")
            # return JsonResponse({'error': "user not present"}, status=400)
        else:
            if check_password(curr_password, self.user.password):                
                print("user present") ###
            else:
                print("invalid current password")
                raise serializers.ValidationError("invalid current password")
                # return JsonResponse({'error': "invalid current password"}, status=400)
        # try:
        #     validate_password(data)
        # except ValidationError as e:
        #     raise serializers.ValidationError(e.messages)

        return data

    def create(self, validated_data):
        # Handle password reset logic here
        self.user.set_password(self.new_password)
        self.user.save()
        print("Password changed.") ###
        return
        # return Response({"message": "Your password is updated."}, status=status.HTTP_200_OK)
