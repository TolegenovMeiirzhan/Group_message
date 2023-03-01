from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *

class RoomForm(forms.ModelForm):
    # participants = forms.ModelMultipleChoiceField
    class Meta:
        model = Room
        fields = ( 'topic', 'name', 'content',)
        widgets ={
            'name': forms.TextInput(attrs={'class': 'form-control'}),

            'topic': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        'class': 'form-control', 'autocomplete': 'off'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'autpcomplete': 'off'}))

class RegisterForm(UserCreationForm):
    # username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
    #     'class': 'form-control', 'autocomplete': 'off'
    # }))
    # first_name = forms.CharField(label='First Name', widget =forms.TextInput(attrs={
    #     'class': 'form-control', 'auto-complete': 'off'
    # }))
    # last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={
    #     'class': 'form-control', 'autocomplete': 'off'
    # }))
    # email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
    #     'class': 'form-control', 'autocomplete': 'off'
    # }))
    # password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
    #     'class': 'form-control', 'autocomplete': 'off'
    # }))
    # password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))

    class META:
        model = User
        fields =('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off'})

        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('body',)