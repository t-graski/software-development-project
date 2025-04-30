# Author: Tobias Graski

from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    ROLE_CHOICES = [
        ('engineer', 'Engineer'),
        ('teamlead', 'Team Leader'),
        ('deptlead', 'Department Leader'),
        ('senior', 'Senior Manager'),
    ]
    roleType = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'roleType']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        fields = ['username', 'password']
