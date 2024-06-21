from django import forms
from app.models import CustomUser
from students.models import Tablestudent, TimeLog

COURSE_CHOICES = [
    ('Computer Science', 'Computer Science'),
    ('Information Technology', 'Information Technology'),
]

class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        email = cleaned_data.get("email")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Password and Confirm Password do not match")

        if CustomUser.objects.filter(email=email).exists():
            self.add_error('email', "Email already exists. Please use a different email address.")
        
        return cleaned_data

class StudentRegistrationForm(forms.ModelForm):
    StudentID = forms.CharField(
        max_length=10, 
        label='Student ID',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Student ID'})
    )

    Course = forms.ChoiceField(
        choices=COURSE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Tablestudent
        fields = ['StudentID', 'Firstname', 'Middlename', 'Lastname', 'Course', 'Year']
        widgets = {
            'Firstname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'Middlename': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter middle name'}),
            'Lastname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'Year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter year'}),
        }

    def __init__(self, *args, **kwargs):
        super(StudentRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['Firstname'].required = True
        self.fields['Middlename'].required = True
        self.fields['Lastname'].required = True
        self.fields['Course'].required = True
        self.fields['Year'].required = True

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current password'})
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', "New password and confirm password do not match")

        return cleaned_data

class TimeLogForm(forms.ModelForm):
    class Meta:
        model = TimeLog
        fields = ['image', 'action']

    def __init__(self, *args, **kwargs):
        super(TimeLogForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = True
        self.fields['image'].widget.attrs.update({'accept': 'image/*'})
        self.fields['action'].widget = forms.HiddenInput()