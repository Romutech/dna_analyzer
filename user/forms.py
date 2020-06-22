from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.ModelForm):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'password')