from django import forms
from .models import AnnouncementTable
from django.contrib.auth import get_user_model
from .custom_widgets import CustomClearableFileInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm

STATUS = [
    ('enable', 'Enable'),
    ('disable', 'Disable'),
]

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'position']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'position']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']

class AnnouncementForm(forms.ModelForm):

    Status = forms.ChoiceField(
        choices=STATUS,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = AnnouncementTable
        fields = ['Title', 'Image', 'Description', 'Status']
        widgets = {
            'Title': forms.TextInput(attrs={'class': 'form-control'}),
            'Description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'Image': CustomClearableFileInput,
        }

        def __init__(self, *args, **kwargs):
            super(AnnouncementForm, self).__init__(*args, **kwargs)
            self.fields['Title'].required = True
            self.fields['Description'].required = True
