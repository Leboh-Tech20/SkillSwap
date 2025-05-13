from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
from .models import Agreement, SkillListing

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'location', 'video_intro_url', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['bio', 'location', 'video_intro_url', 'profile_image']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'video_intro_url': forms.URLInput(attrs={'class': 'form-control'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }
class AgreementForm(forms.ModelForm):
    class Meta:
        model = Agreement
        fields = ['responder', 'requested_skill', 'start_date', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional message or expectations...'}),
        }
