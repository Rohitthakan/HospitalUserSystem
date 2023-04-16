from django import forms
from django.contrib.auth.models import User
from users.models import UserProfileInfo
from datetime import datetime, date

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'first_name', 'last_name','password')
        widgets = {
            'password': forms.PasswordInput(attrs={'id': 'password-input', 'class': 'form-control'}),
        }

class UserProfileInfoForm(forms.ModelForm):
    confirmPassword = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    class Meta():
        model = UserProfileInfo
        fields = ('confirmPassword','type', 'address')
        widgets = {
            'confirmPassword': forms.PasswordInput(attrs={'id': 'confirmPassword-input', 'class': 'form-control', 'name' : 'confirmPassword'}),
            # 'document' : forms.FileInput(attrs={'name': 'document'}),
            'type': forms.Select(attrs={'name' : 'type'}),
            'address' : forms.TextInput(attrs={'name' : 'address'})
        }





