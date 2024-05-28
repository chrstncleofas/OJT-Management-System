from django import forms
from app.models import CustomUser
from students.models import TableStudents, TimeLog

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

class StudentRegistrationForm(forms.ModelForm):
    StudentID = forms.CharField(max_length=10, label='Student ID')

    class Meta:
        model = TableStudents
        fields = ['StudentID', 'Firstname', 'Lastname', 'Course', 'Year']

    def __init__(self, *args, **kwargs):
        super(StudentRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['Firstname'].required = True
        self.fields['Lastname'].required = True
        self.fields['Course'].required = True
        self.fields['Year'].required = True

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

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
        fields = ['action', 'image']
        widgets = {
            'action': forms.HiddenInput(),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
