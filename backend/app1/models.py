from django.db import models

# Create your models here.

industryTypes = (('arts', 'ARTS'), ('music', 'MUSIC'), ('acting', 'ACTING'))

class Client(models.Model) :
    org_name = models.CharField(max_length=100)
    industry = models.CharField(max_length=50, choices=industryTypes, default='arts')
    address = models.CharField(max_length=250)

class Creator(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    address = models.CharField(max_length=250)
    field = models.CharField(max_length=10, choices=industryTypes, default='arts')
    pronounTypes = (('H', 'He'), ('S', 'She'), ('O', 'Other'))
    pronoun = models.CharField(max_length=10, choices=pronounTypes, default='O')
