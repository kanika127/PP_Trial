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
# Create your models here.

def validate_email(email) :
    r = EmailValidator(email)
    print('EMAIL validator called')
    print(r)
    raise ValidationError('inv email addr')

class MyClient(models.Model) :
    org_name = models.CharField(max_length=50, default="")
    industry = models.CharField(max_length=50, default="")
    address = models.CharField(max_length=50, default="")
    email = models.EmailField(max_length=50) #, validators=[EmailValidator('inv email')]) NOT REQD ---> JUST DO 'full_clean' before model_obj.save()
    mobile = PhoneNumberField(null=False, blank=False)



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

    
# industryTypes = (('arts', 'ARTS'), ('music', 'MUSIC'), ('acting', 'ACTING')) ## check if options or subjective
def validate_phone_number(value):
    min_value = 1000000000  # Minimum 10 digit number
    max_value = 9999999999  # Maximum 10 digit number
    if not (min_value <= value <= max_value):
        raise ValidationError(f'{value} is not a valid 10-digit phone number.')

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
class Project(models.Model) :
    # owner = models.ForeignKey(PassionUser, on_delete=models.CASCADE, related_name='pitched_projects', default=PassionUser.objects.get(username="kanika127@gmail.com")) ## will delete project when user is deleted
    owner = models.ForeignKey(PassionUser, on_delete=models.CASCADE, related_name='pitched_projects', null=False) ## will delete project when user is deleted
    title = models.CharField(max_length=100)
    medium = models.CharField(max_length=100)
    approx_completion_date = models.DateField()
    description = models.CharField(max_length=2000)
    # collab_types = (('P', 'Paid'), ('U', 'Unpaid'), ('C', 'Collaboration')) ## check options
    # collab_type = models.CharField(max_length=15, choices=collab_types, default='Collaboration')
    sample_work = models.CharField(max_length=1000) ## check meaning and datatype
    # role_count = models.IntegerField(_("1")) ## check if its default type
    role_count = models.IntegerField()
    # role_type = ## add role types for each role
    # role_budget = ## add role budgets for ecah role
    collab_types = (('I', 'In-person'), ('V', 'Virtual'), ('H', 'Hybrid')) ## check Hybrid
    mode = models.CharField(max_length=10, choices=collab_types, default='Hybrid')

class Role(models.Model) :
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='roles', null=False)
    role_type = models.CharField(max_length=50)
    collab_types = (('P', 'Paid'), ('U', 'Unpaid'), ('C', 'Collaboration')) ## check options
    collab_type = models.CharField(max_length=15, choices=collab_types, default='Collaboration')
    budget = models.FloatField()
    exec_modes = (('P', 'in-person'), ('V', 'virtual'))
    exec_mode = models.CharField(max_length=15, choices=exec_modes)  #, default='virtual')

class Application(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='applications')
    # applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=100, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')))
    submission_date = models.DateTimeField(auto_now_add=True) ## check
    # any other fields relevant to the application

#user = User.objects.get(username='nikki')
# table1_entry = Creator(first_name='Nikki', user=user)
# table1_entry.save()


class tmptable(models.Model) :
    user = models.CharField(max_length=50) ## check
    title = models.CharField(max_length=100)
    medium = models.CharField(max_length=100, blank=False, default=None)
    org_name = models.CharField(max_length=100, default="")

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)
    class Meta :
        abstract = True


class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)
