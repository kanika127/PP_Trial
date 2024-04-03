from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from polymorphic.models import PolymorphicModel, PolymorphicManager
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField

from abc import ABC, ABCMeta
import os
# Create your models here.

def validate_email(email) :
    r = EmailValidator(email)
    raise ValidationError('inv email addr')

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

class MyUserManager(BaseUserManager, PolymorphicManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        my_user = self.model(email=email, username=email, **extra_fields)
        my_user.set_password(password)
        my_user.save()
        return my_user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    
class PassionUser(AbstractUser, PolymorphicModel) :
    email = models.EmailField(unique=True) # required to make email unique.
    mobile = PhoneNumberField(null=False, blank=True)
    # location = TODO
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True) ## TODO: check working
    bio = models.TextField(blank=True)
    sample_work = models.CharField(max_length=5000, null=False, blank=True)
    objects = MyUserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile', 'sample_work']

    def __str__(self):
        return self.email

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
    
## TODO: check max_length for all
## TODO: remove null from phone and email
class Creator(PassionUser) :
    # field = models.CharField(max_length=100, choices=industryTypes, default='arts') ## TODO: ASK: check datatype
    # field = models.CharField(max_length=100, default='') ## TODO: ASK: check datatype
    field = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    pronounTypes = (('H', 'He'), ('S', 'She'), ('O', 'Other')) ## TODO: ASK: check options
    pronoun = models.CharField(max_length=10, choices=pronounTypes, default='O')
    star_rating = models.FloatField()
    # past_projects = models.ManyToManyField(Project, related_name='creator_projects')
    roles = models.ManyToManyField('Role', related_name='creator_roles')

    def __str__(self):
        return self.username
        # return self.user.username


##### TODO: PROJECT FIELDS CHECK
class SampleWrkTbl(models.Model) :
    text = models.CharField(max_length=100)
    link = models.URLField('sample_wrk_link', max_length=128) #, db_index=True, unique=True)

class Project(models.Model) :
    # owner = models.ForeignKey(PassionUser, on_delete=models.CASCADE, related_name='pitched_projects', default=PassionUser.objects.get(username="kanika127@gmail.com")) ## will delete project when user is deleted
    owner = models.ForeignKey(PassionUser, on_delete=models.CASCADE, related_name='pitched_projects', blank=False, default=None ) ## will delete project when user is deleted
    title = models.CharField(max_length=100, blank=False, default=None )
    medium = models.CharField(max_length=100, blank=False, default=None )
    approx_completion_date = models.DateField(blank=False, default=None )
    description = models.CharField(max_length=2000, blank=False, default=None )
    sample_wrk = models.ForeignKey(SampleWrkTbl, on_delete=models.CASCADE, related_name='sample_work', blank=False, default=None )

    class Status(models.TextChoices) :
        PENDING = 'P', 'Pending'
        LIVE = 'L', 'Live'
        MATCH_SUCCESS = 'MS', 'MatchSuccess'
        NO_MATCHES = 'NM', 'NoMatches'
        COMPLETE = 'C', 'Complete'
    project_status = models.CharField(max_length=3, choices=Status.choices, blank=False, default=None)


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
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='roles', blank=False, default=None)
    role_type = models.CharField(max_length=5, choices=DynamicRoleChoices.get_choices(), default=DynamicRoleChoices._choices[0][0])
    other_role_type = models.CharField(max_length=100, blank=True, null=True) # extra fld to save data if 'status' is 'other'
    
    def save(self, *args, **kwargs) :
        if self.role_type != DynamicRoleChoices.OTHER:
            self.other_role_type = ''  # Clear the other_status if 'Other' is not selected
        elif self.other_role_type == None :
            raise ValidationError('data not specified for "other" type')
        super().save(*args, **kwargs)

    role_count = models.IntegerField() #default kwargs make it a required field

    class CollabTypes(models.TextChoices) :
        PAID = 'P', 'Paid'
        UNPAID = 'U', 'Unpaid'
        COLLABORATION = 'C', 'Collaboration'
    collab_type = models.CharField(max_length=15, choices=CollabTypes.choices, default=CollabTypes.PAID)

    budget = models.FloatField() #default kwargs make it a required field
    
    class ExecModes(models.TextChoices) :
        IN_PERSON = 'P', 'in-person'
        VIRTUAL = 'V', 'virtual'
    exec_mode = models.CharField(max_length=15, choices=ExecModes.choices, default=ExecModes.IN_PERSON)  #, default='virtual')

class Application(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='applications', blank=False, default=None)
    applicant = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='applications', blank=False, default=None)
    # applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    submission_date = models.DateTimeField(auto_now_add=True) ## check
    # any other fields relevant to the application

    class ApplicationStatus(models.TextChoices) :
        PENDING = 'P', 'Pending'
        APPROVED = 'A', 'Approved'
        REJECTED = 'R', 'Rejected'
        OTHER = 'O', 'Other'
    application_status = models.CharField(max_length=10, choices=ApplicationStatus.choices, default=ApplicationStatus.PENDING)


#user = User.objects.get(username='nikki')
# table1_entry = Creator(first_name='Nikki', user=user)
# table1_entry.save()

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)
    class Meta :
        abstract = True


class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)
