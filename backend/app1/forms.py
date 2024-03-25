from django import forms
from .models import PassionUser, Creator, Client

class PassionUserProfileForm(forms.ModelForm):
    class Meta:
        model = PassionUser
        fields = ['mobile', 'profile_picture', 'bio', 'sample_work']  # Fields to be updated in the user profile

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if not mobile:
            raise forms.ValidationError("Mobile field cannot be blank.")
        return mobile

    def clean_sample_work(self):
        sample_work = self.cleaned_data['sample_work']
        if not sample_work:
            raise forms.ValidationError("Sample work field cannot be blank.")
        return sample_work

# Form for Creator with specific fields
class CreatorForm(PassionUserProfileForm):
    class Meta(PassionUserProfileForm.Meta):
        model = Creator
        fields = PassionUserProfileForm.Meta.fields + ['field', 'pronoun', 'star_rating']


# Form for Client with specific fields
class ClientForm(PassionUserProfileForm):
    class Meta(PassionUserProfileForm.Meta):
        model = Client
        fields = PassionUserProfileForm.Meta.fields + ['org_name', 'industry']