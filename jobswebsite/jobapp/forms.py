from django import forms
from .models import Resume, Resume, JobApplication, Company


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'skills', 'experience', 'education']


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['resume', 'cover_letter']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['resume'].queryset = Resume.objects.filter(user=user)


class CompanyRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Company
        fields = ['name', 'number']
