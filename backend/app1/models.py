from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator, MinValueValidator, MaxValueValidator
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

class EmailVerificationToken(models.Model):
    email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    user_data = models.JSONField(default=dict)  # For storing user details
    verification_code = models.CharField(max_length=6, default="123456") ## TODO: remove default
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} - {self.token}"

class UserSampleWorkTable(models.Model) :
    def validate_file_extension(value):
        ext = os.path.splitext(value.name)[1]  # Get the file extension
        valid_extensions = ['.jpg', '.jpeg', '.png', '.mp4', '.mov', '.mp3', '.HEIC', '.wav', '.m4a', '.pdf']
        if not ext.lower() in valid_extensions:
            raise ValidationError('Unsupported file extension.')

    CONTENT_TYPES = (
        # ('music', 'Music File'),
        # ('video', 'Video File'),
        # ('photo', 'Photo File'),
        # ('pdf', 'PDF File'),
        ('file', 'File'),
        ('link', 'Link'),
    )

    # user = models.ForeignKey('PassionUser', on_delete=models.CASCADE, related_name='sample_works', default=User.objects.get(pk=1))
    text = models.CharField(max_length=100)
    description = models.CharField(max_length=2000, blank=False, default=None)
    content_type = models.CharField(max_length=5, choices=CONTENT_TYPES, blank=True, null=True)
    content_file = models.FileField(upload_to='user_sample_work_content/', validators=[validate_file_extension], blank=True, null=True)
    link = models.URLField(max_length=200, blank=True, null=True)
    cover_picture = models.ImageField(upload_to='sample_work_cover_pics/', blank=True, null=True) 

class MyUserManager(BaseUserManager, PolymorphicManager):
    def create_user(self, username, password=None, **extra_fields):
    # def create_user(self, username, email=email, password=None, **extra_fields):
        # if not email:
        #     raise ValueError('The Email field must be set')
        # email = self.normalize_email(email)
        my_user = self.model(username=username, **extra_fields)
        my_user.set_password(password)
        my_user.save()
        return my_user

    def create_superuser(self, username,  password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        # return self.create_user(username, password, **extra_fields)
        #SuperUser._default_manager.create(username, password, **extra_fields)
        self.create_user(username, password, **extra_fields)
    
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

    class Meta :
        verbose_name = 'Super User'
    def __str__(self):
        return self.username

class PassionUser(BaseUser) :
    bio = models.TextField(blank=True)
    sample_work_1 = models.ForeignKey(UserSampleWorkTable, on_delete=models.CASCADE, related_name='user_sample_work_1', blank=True, null=True, default=None)
    sample_work_2 = models.ForeignKey(UserSampleWorkTable, on_delete=models.CASCADE, related_name='user_sample_work_2', blank=True, null=True, default=None)
    sample_work_3 = models.ForeignKey(UserSampleWorkTable, on_delete=models.CASCADE, related_name='user_sample_work_3', blank=True, null=True, default=None)
    # REQUIRED_FIELDS = ['sample_work_1']

    def __str__(self):
        return self.username
    class Meta :
        verbose_name = 'Passion User'
        verbose_name_plural = 'Passion Users'
    # class Meta :
    #     abstract = True

class Client(PassionUser) : 
    org_name = models.CharField(max_length=100, default="")
    # industry = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    industry = models.CharField(max_length=100, default='') ## TODO: ASK: check datatype
    other_industry = models.CharField(max_length=100, default="")
    # industry = models.CharField(max_length=50, choices=industryTypes, default='arts') ## TODO: ASK: check datatype
    # past_projects = models.ManyToManyField(Project, related_name='client_projects')

    def __str__(self):
        return self.username
    class Meta :
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
    
## TODO: check max_length for all
## TODO: remove null from phone and email
class Creator(PassionUser) :
    field = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    other_field = models.CharField(max_length=100, default="")
    pronounTypes = (('H', 'He'), ('S', 'She'), ('O', 'Other')) ## TODO: ASK: check options
    pronoun = models.CharField(max_length=10, choices=pronounTypes, default='O')
    star_rating = models.FloatField(default = 0)
    skills = ArrayField(models.CharField(max_length=200), size=5, blank=True, default=list) ## TODO
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

class ProjectSampleWorkTable(models.Model) :
    text = models.TextField(max_length=100)
    link = models.URLField('sample_wrk_link', max_length=128, blank=True, null=True) #, db_index=True, unique=True)

    def clean(self):
        if self.link:
            validate = URLValidator()
            try:
                validate(self.link)
            except ValidationError as e:
                raise ValidationError("Invalid URL provided.")
        super().clean()

    def __str__(self):
        return f"Sample Work: {self.text[:50]}..."  # Display first 50 characters

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

    def __str__(self) : return f'{self.title}    BY    {self.owner.username}'

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
        #print(cls._choices)
        return cls._choices

ROLE_CHOICES = DynamicRoleChoices.get_choices()

class RoleQuestion(models.Model) :
    class Status(models.TextChoices) :
        IMAGE = 'I', 'Image'
        VIDEO = 'V', 'Video'
        FILE = 'F', 'File'
        TEXTBOX = 'T', 'Textbox'

    prompt = models.CharField(max_length=100, blank=True)
    guidelines = models.CharField(max_length=2000, blank=True, null=True)
    content_type = models.CharField(max_length=5, choices=Status.choices, default=Status.TEXTBOX)

    def __str__(self) :
        return f'{self.prompt}'

class Role(models.Model) :
    class CollabTypes(models.TextChoices) :
        PAID = 'P', 'Paid'
        UNPAID = 'U', 'Unpaid'
        COLLABORATION = 'C', 'Collaboration'
    
    class ExecModes(models.TextChoices) :
        IN_PERSON = 'P', 'in-person'
        VIRTUAL = 'V', 'virtual'
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='roles', blank=False, default=None)
    role_type = models.CharField(max_length=5, choices=ROLE_CHOICES, default=ROLE_CHOICES[0][0])
    other_role_type = models.CharField(max_length=100, blank=True, null=True) # extra field to save data if 'status' is 'other'
    role_count = models.IntegerField(default = 1, validators=[MinValueValidator(1), MaxValueValidator(10)]) #default kwargs make it a required field
    no_of_matches = models.IntegerField(default=0) # to be incremented on match and decremented if someone leaves
    collab_type = models.CharField(max_length=15, choices=CollabTypes.choices, default=CollabTypes.PAID)
    budget = models.FloatField(default = 0) 
    budget_visibility = models.BooleanField(default = False) 
    exec_mode = models.CharField(max_length=15, choices=ExecModes.choices, default=ExecModes.IN_PERSON)  #, default='virtual')
    question_1 = models.ForeignKey(RoleQuestion, on_delete=models.CASCADE, related_name='role_question_1', null=True, default=None)
    question_2 = models.ForeignKey(RoleQuestion, on_delete=models.CASCADE, related_name='role_question_2', null=True, default=None)
    question_3 = models.ForeignKey(RoleQuestion, on_delete=models.CASCADE, related_name='role_question_3', null=True, default=None)
    

    class Meta :
        unique_together = ('project', 'role_type')

    def clean(self):
        # Ensure no_of_matches does not exceed role_count
        if self.no_of_matches > self.role_count:
            raise ValidationError({
                'no_of_matches': 'The number of matches cannot exceed the role count.'
            })
        
        # Check if budget is required
        if self.collab_type == self.CollabTypes.PAID and self.budget is None:
            raise ValidationError({'budget': 'Budget is required when collaboration type is "Paid".'})
        # Optionally, check if budget should be zero or not set for non-paid types
        if self.collab_type != self.CollabTypes.PAID and self.budget is not None:
            if self.budget != 0:
                raise ValidationError({'budget': 'Budget should be zero or unset for unpaid or collaboration projects.'})


    def save(self, *args, **kwargs) :
        if self.role_type != DynamicRoleChoices.OTHER:
            self.other_role_type = ''  # Clear the other_status if 'Other' is not selected
        elif self.other_role_type == None :
            raise ValidationError('data not specified for "other" type')
        super().save(*args, **kwargs)

    def __str__(self) : return f'{self.role_type=}, {self.project=}'

class ApplicationQuestion(models.Model) :
    def validate_file_extension(value):
        ext = os.path.splitext(value.name)[1]  # Get the file extension
        valid_extensions = ['.jpg', '.jpeg', '.png', '.mp4', '.mov', '.mp3', '.HEIC', '.wav', '.m4a', '.pdf']
        if not ext.lower() in valid_extensions:
            raise ValidationError('Unsupported file extension.')

    text = models.CharField(max_length=100)
    content_file = models.FileField(upload_to='user_sample_work_content/', validators=[validate_file_extension], blank=True, null=True)

class Application(models.Model):
    class ApplicationStatus(models.TextChoices) :
        PENDING = 'P', 'Pending'
        PROSPECT = 'PUR', 'Prospect - Under Review'
        APPROVED = 'A', 'Approved'
        REJECTED = 'R', 'Rejected'
        NON_PROSPECT = 'NPS', 'Non-Prospect'
        SCREENING = 'S', 'Screening'

    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='applications', blank=False, default=None)
    applicant = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='applications', blank=False, default=None)
    submission_date = models.DateTimeField(auto_now_add=True) ## check
    # any other fields relevant to the application
    application_status = models.CharField(max_length=10, choices=ApplicationStatus.choices, default=ApplicationStatus.PENDING) # ignores data sent by user
    ques_1_content = models.ForeignKey(ApplicationQuestion, on_delete=models.CASCADE, related_name='application_content_1', null=True, default=None)
    ques_2_content = models.ForeignKey(ApplicationQuestion, on_delete=models.CASCADE, related_name='application_content_2', null=True, default=None)
    ques_3_content = models.ForeignKey(ApplicationQuestion, on_delete=models.CASCADE, related_name='application_content_3', null=True, default=None)

    def validate_content_file(self, content, role_question):
        if content and self.role and role_question:
            content_file = content.content_file
            content_type = role_question.content_type
            if content_type == 'T':
                if not content.text:
                    raise ValidationError(f'No text entered when content type is {role_question.content_type}.')
                    # raise ValidationError(f'No text entered when content type is {role_question.get_content_type_display()}.')
            elif content_file:  # Ensure there is a file uploaded
                ext = os.path.splitext(content_file.name)[-1]  # Get the file extension
                
                # Map content types to valid extensions
                extension_map = {
                    'I': ['.jpg', '.jpeg', '.png', '.heic'],
                    'V': ['.mp4', '.mov'],
                    'F': ['.pdf'],
                }

                valid_extensions = extension_map.get(content_type, [])

                if not ext.lower() in valid_extensions:
                    raise ValidationError(f'Invalid file extension for content type {role_question.content_type}. Allowed extensions are: {valid_extensions}')
                    # raise ValidationError(f'Invalid file extension for content type {role_question.get_content_type_display()}. Allowed extensions are: {valid_extensions}')

    def clean(self):
        question_contents = [self.ques_1_content, self.ques_2_content, self.ques_3_content]
        role_questions = [self.role.question_1, self.role.question_2, self.role.question_3]

        for content, role_question in zip(question_contents, role_questions):
            if content and role_question:
                self.validate_content_file(content, role_question)

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure validation is called
        super().save(*args, **kwargs)

    class Meta :
        unique_together = ('applicant', 'role')

    def __str__(self) : return f'Application by {self.applicant.username} for role -> {self.role.role_type}'

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
