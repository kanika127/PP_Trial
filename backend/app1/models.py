from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.models import User

# Create your models here.


# industryTypes = (('arts', 'ARTS'), ('music', 'MUSIC'), ('acting', 'ACTING')) ## check if options or subjective
def validate_phone_number(value):
    min_value = 1000000000  # Minimum 10 digit number
    max_value = 9999999999  # Maximum 10 digit number
    if not (min_value <= value <= max_value):
        raise ValidationError(f'{value} is not a valid 10-digit phone number.')

## TODO: check industry/field datatype
## TODO: check max_length for all
## TODO: remove null from phone and email
class Creator(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = User.objects.get(username='nikki')
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    mobile = models.IntegerField(validators=[validate_phone_number], help_text="Enter a 10-digit phone number", null=True) ## TODO: verify validity
    email = models.CharField(max_length=255, validators=[EmailValidator()], null=True) ## TODO: verify validity 
    # field = models.CharField(max_length=100, choices=industryTypes, default='arts') ## TODO: ASK: check datatype
    field = models.CharField(max_length=100, default='') ## TODO: ASK: check datatype
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True) ## TODO: check working
    bio = models.CharField(max_length=1000, default="")
    sample_work = models.CharField(max_length=5000, null=True)
    pronounTypes = (('H', 'He'), ('S', 'She'), ('O', 'Other')) ## TODO: ASK: check options
    pronoun = models.CharField(max_length=10, choices=pronounTypes, default='O')

    def __str__(self):
        return self.user.username

class Client(models.Model) :
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    mobile = models.IntegerField(validators=[validate_phone_number], help_text="Enter a 10-digit phone number", null=True) ## TODO: verify validity
    email = models.CharField(max_length=255, validators=[EmailValidator()], null=True) ## TODO: verify validity 
    org_name = models.CharField(max_length=100, default="")
    # industry = models.CharField(max_length=50, choices=industryTypes, default='arts') ## TODO: ASK: check datatype
    industry = models.CharField(max_length=100, default='') ## TODO: ASK: check datatype
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True) ## TODO: check working
    bio = models.CharField(max_length=1000, default="")
    sample_work = models.CharField(max_length=5000, null=True)

    def __str__(self):
        return self.user.username   


##### TODO: PROJECT FIELDS CHECK
class Project(models.Model) :
    user = models.CharField(max_length=50) ## check
    title = models.CharField(max_length=100)
    medium = models.CharField(max_length=100)
    approx_completion_date = models.DateField()
    description = models.CharField(max_length=2000)
    collab_types = (('P', 'Paid'), ('U', 'Unpaid'), ('C', 'Collaboration')) ## check options
    collab_type = models.CharField(max_length=15, choices=collab_types, default='Collaboration')
    sample_work = models.CharField(max_length=1000) ## check meaning and datatype
    # role_count = models.IntegerField(_("1")) ## check if its default type
    role_count = models.IntegerField()
    # role_type = ## add role types for each role
    # role_budget = ## add role budgets for ecah role
    collab_types = (('I', 'In-person'), ('V', 'Virtual'), ('H', 'Hybrid')) ## check Hybrid
    mode = models.CharField(max_length=10, choices=collab_types, default='Hybrid')

user = User.objects.get(username='nikki')
# table1_entry = Creator(first_name='Nikki', user=user)
# table1_entry.save()