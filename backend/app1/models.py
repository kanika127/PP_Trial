from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.models import User

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

##### TODO: PROJECT FIELDS CHECK
class Project(models.Model) :
    # user = models.CharField(max_length=50) ## check
    # project_owner = 
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
    role_type = models.CharField(max_length=50)
    collab_types = (('P', 'Paid'), ('U', 'Unpaid'), ('C', 'Collaboration')) ## check options
    collab_type = models.CharField(max_length=15, choices=collab_types, default='Collaboration')
    budget = models.FloatField()
    exec_modes = (('P', 'in-person'), ('V', 'virtual'))
    exec_mode = models.CharField(max_length=15, choices=exec_modes)  #, default='virtual')

class PassionUser(User) :
    mobile = PhoneNumberField(null=False, blank=False)
    # location = TODO
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True) ## TODO: check working
    bio = models.CharField(max_length=1000, default="")
    sample_work = models.CharField(max_length=5000, null=True)

    class Meta :
        abstract = True

class Client(PassionUser) : #models.Model) :
    org_name = models.CharField(max_length=100, default="")
    # industry = models.CharField(max_length=50, choices=industryTypes, default='arts') ## TODO: ASK: check datatype
    industry = models.CharField(max_length=100, default='') ## TODO: ASK: check datatype
    past_projects = models.ManyToManyField(Project, related_name='client_projects')

    def __str__(self):
        return self.username   


# industryTypes = (('arts', 'ARTS'), ('music', 'MUSIC'), ('acting', 'ACTING')) ## check if options or subjective
def validate_phone_number(value):
    min_value = 1000000000  # Minimum 10 digit number
    max_value = 9999999999  # Maximum 10 digit number
    if not (min_value <= value <= max_value):
        raise ValidationError(f'{value} is not a valid 10-digit phone number.')

## TODO: check industry/field datatype
## TODO: check max_length for all
## TODO: remove null from phone and email
class Creator(PassionUser) :
    # field = models.CharField(max_length=100, choices=industryTypes, default='arts') ## TODO: ASK: check datatype
    field = models.CharField(max_length=100, default='') ## TODO: ASK: check datatype
    pronounTypes = (('H', 'He'), ('S', 'She'), ('O', 'Other')) ## TODO: ASK: check options
    pronoun = models.CharField(max_length=10, choices=pronounTypes, default='O')
    star_rating = models.FloatField()
    past_projects = models.ManyToManyField(Project, related_name='creator_projects')

    def __str__(self):
        return self.user.username

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
