from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager, User
from polymorphic.models import PolymorphicModel, PolymorphicManager
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
import uuid
# from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

from phonenumber_field.modelfields import PhoneNumberField

from abc import ABC, ABCMeta
import os
# Create your models here.

def validate_email(email) :
    r = EmailValidator(email)
    raise ValidationError('inv email addr')

class EmailVerificationToken(models.Model):
    email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    user_data = models.JSONField(default=dict)  # For storing user details

    def __str__(self):
        return f"{self.email} - {self.token}"

class UserSampleWorkTable(models.Model) :
    def validate_file_extension(value):
        ext = os.path.splitext(value.name)[1]  # Get the file extension
        valid_extensions = ['.jpg', '.jpeg', '.png', '.mp4', '.mp3', '.wav']
        if not ext.lower() in valid_extensions:
            raise ValidationError('Unsupported file extension.')
    
    text = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/', validators=[validate_file_extension])

class MyUserManager(BaseUserManager, PolymorphicManager):
    def create_user(self, username, password=None, **extra_fields):
    # def create_user(self, username, email=email, password=None, **extra_fields):
        # if not email:
        #     raise ValueError('The Email field must be set')
        # email = self.normalize_email(email)
        my_user = self.model(username=username, **extra_fields)
        # my_user = self.model(username=username, email=email, **extra_fields)
        my_user.set_password(password)
        my_user.save()
        return my_user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, password, **extra_fields)
    
class BaseUser(AbstractUser, PolymorphicModel) :
    email = models.EmailField(unique=True) # required to make email unique.
    mobile = PhoneNumberField(null=False, blank=True)
    # location = TODO
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True) ## TODO: check working
    objects = MyUserManager()
    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['mobile', 'sample_work']
    REQUIRED_FIELDS = ['mobile']

    def __str__(self):
        return self.username

    # class Meta :
    #     abstract = True

class SuperUser(BaseUser) :
    admin_level = models.CharField(max_length=100, default='standard')

    def __str__(self):
        return self.username

class PassionUser(BaseUser) :
    bio = models.TextField(blank=True)
    # sample_work = models.CharField(max_length=5000, null=False, blank=True) 
    # sample_work = models.ForeignKey(UserSampleWorkTable, on_delete=models.CASCADE, related_name='user_sample_work', blank=False, default=None)
    sample_work = models.ForeignKey(UserSampleWorkTable, on_delete=models.CASCADE, related_name='user_sample_work', null=True, default=None)
    # REQUIRED_FIELDS = ['sample_work']

    def __str__(self):
        return self.username
    # class Meta :
    #     abstract = True

class Client(PassionUser) : 
    org_name = models.CharField(max_length=100, default="")
    industry = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    # industry = models.CharField(max_length=50, choices=industryTypes, default='arts') ## TODO: ASK: check datatype
    # industry = models.CharField(max_length=100, default='') ## TODO: ASK: check datatype
    # past_projects = models.ManyToManyField(Project, related_name='client_projects')

    def __str__(self):
        return self.username
    class Meta :
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
    
## TODO: check max_length for all
## TODO: remove null from phone and email
class Creator(PassionUser) :
    field = ArrayField(models.CharField(max_length=200), blank=True, default=list) ## TODO
    pronounTypes = (('H', 'He'), ('S', 'She'), ('O', 'Other')) ## TODO: ASK: check options
    pronoun = models.CharField(max_length=10, choices=pronounTypes, default='O')
    star_rating = models.FloatField(default = 0)
    # past_projects = models.ManyToManyField(Project, related_name='creator_projects')
    # roles = models.ManyToManyField('Role', related_name='creator_roles')

    def __str__(self):
        return self.username
        # return self.user.username
    class Meta :
        verbose_name = 'Creator'
        verbose_name_plural = 'Creators'

class PhoneVerification(models.Model):
    # mobile = models.CharField(max_length=10, unique=True)
    mobile = models.CharField(unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    # expires_at = models.DateTimeField()

    def is_valid(self, submitted_code):
        return submitted_code == self.code and timezone.now() < self.created_at + timedelta(minutes=5)
        # return self.code == submitted_code and timezone.now() < self.expires_at

############# MUM models start here ######################################
##### TODO: PROJECT FIELDS CHECK
class ProjectSampleWorkTable(models.Model) :
    text = models.CharField(max_length=100)
    link = models.URLField('sample_wrk_link', max_length=128) #, db_index=True, unique=True)
    # sample_wrk_id = models.CharField(max_length=100, primary_key=True)

class Project(models.Model) :
    class Status(models.TextChoices) :
        PENDING = 'PG', 'Pending'
        LIVE = 'L', 'Live'
        COMPLETE = 'C', 'Complete'
        PAUSE = 'PS', 'Pause'

    owner = models.ForeignKey(PassionUser, on_delete=models.CASCADE, related_name='projects', blank=False, default=None )
    title = models.CharField(max_length=100, blank=False, default=None )
    medium = models.CharField(max_length=100, blank=False, default=None )
    approx_completion_date = models.DateField(blank=False, default=None )
    description = models.CharField(max_length=2000, blank=False, default=None )
    sample_wrk = models.ForeignKey(ProjectSampleWorkTable, on_delete=models.CASCADE, related_name='project_sample_work', blank=False, default=None )
    project_status = models.CharField(max_length=3, choices=Status.choices, blank=False, default=Status.PENDING)

    class Meta :
        unique_together = ('owner', 'title')

    def __str__(self) : return self.title

class DynamicRoleChoices :
    _choices = []
    _last_loaded = 0
    roles_fpath = 'app1/role_choices.cfg'
    OTHER = None

    @classmethod
    def load_choices(cls):
        mod_time = os.path.getmtime(cls.roles_fpath)
        if mod_time > cls._last_loaded:
            cls._choices = []
            cls._choices = [tuple(line.strip().lstrip("'").split(',')) for line in open(cls.roles_fpath)]
            cls._last_loaded = mod_time
            cls.OTHER = cls._choices[-1][0]

    @classmethod
    def get_choices(cls):
        cls.load_choices()
        return cls._choices

class Role(models.Model) :
    class CollabTypes(models.TextChoices) :
        PAID = 'P', 'Paid'
        UNPAID = 'U', 'Unpaid'
        COLLABORATION = 'C', 'Collaboration'
    
    class ExecModes(models.TextChoices) :
        IN_PERSON = 'P', 'in-person'
        VIRTUAL = 'V', 'virtual'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='roles', blank=False, default=None)
    role_type = models.CharField(max_length=5, choices=DynamicRoleChoices.get_choices(), default=DynamicRoleChoices._choices[0][0])
    other_role_type = models.CharField(max_length=100, blank=True, null=True) # extra fld to save data if 'status' is 'other'
    role_count = models.IntegerField() #default kwargs make it a required field
    no_of_matches = models.IntegerField(default=0) # to be incremented on match
    collab_type = models.CharField(max_length=15, choices=CollabTypes.choices, default=CollabTypes.PAID)
    budget = models.FloatField() #default kwargs make it a required field
    exec_mode = models.CharField(max_length=15, choices=ExecModes.choices, default=ExecModes.IN_PERSON)  #, default='virtual')

    class Meta :
        unique_together = ('project', 'role_type')
    
    def save(self, *args, **kwargs) :
        if self.role_type != DynamicRoleChoices.OTHER:
            self.other_role_type = ''  # Clear the other_status if 'Other' is not selected
        elif self.other_role_type == None :
            raise ValidationError('data not specified for "other" type')
        super().save(*args, **kwargs)

    def __str__(self) : return f'{self.role_type=}, {self.project=}'

class MatchedUsers(models.Model):
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role', blank=False, default=None)
    owner = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='matched_users', blank=False, default=None )
    class Meta:
        unique_together = ('role_id', 'owner')

class Application(models.Model):
    class ApplicationStatus(models.TextChoices) :
        PENDING = 'P', 'Pending'
        APPROVED = 'A', 'Approved'
        REJECTED = 'R', 'Rejected'

    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='applications', blank=False, default=None)
    applicant = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='applications', blank=False, default=None)
    submission_date = models.DateTimeField(auto_now_add=True) ## check
    # any other fields relevant to the application
    application_status = models.CharField(max_length=10, choices=ApplicationStatus.choices, default=ApplicationStatus.PENDING)
    ques = models.CharField(max_length=1000, blank=True) 

    class Meta :
        unique_together = ('applicant', 'role')

    def __str__(self) : return f'Application by {self.applicant.username} for role -> {self.role.role_type}'

############### MUM temp test models

class MyClient(models.Model) :
    org_name = models.CharField(max_length=50, default="")
    industry = models.CharField(max_length=50, default="")
    address = models.CharField(max_length=50, default="")
    email = models.EmailField(max_length=50) #, validators=[EmailValidator('inv email')]) NOT REQD ---> JUST DO 'full_clean' before model_obj.save()
    mobile = PhoneNumberField(null=False, blank=False)

    class Status(models.TextChoices) :
        PENDING = 'P', 'Pending'
        APPROVED = 'A', 'Approved'
        REJECTED = 'R', 'Rejected'
        OTHER = 'O', 'Other'
        #choices = models.ChoicesType(('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected'), ('O', 'Other'))
    application_status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    other_status = models.CharField(max_length=100, blank=True, null=True) # extra fld to save data if 'status' is 'other'
    
    def save(self, *args, **kwargs) :
        if self.application_status != MyClient.Status.OTHER:
            self.other_status = ''  # Clear the other_status if 'Other' is not selected
        super().save(*args, **kwargs)

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)
    class Meta :
        abstract = True

class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)
