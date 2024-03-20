from django import forms
from .models import Creator

class CreatorForm(forms.ModelForm):
    class Meta:
        model = Creator
        fields = ['first_name','last_name','mobile','email','field','profile_picture','bio','sample_work','pronoun']