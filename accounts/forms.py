from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    fname = forms.CharField(max_length=150, required=True, label='First name')
    lname = forms.CharField(max_length=150, required=True, label='Last name')

    class Meta:
        model = User
        fields = ("username", "email", "fname", "lname", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['fname'].help_text = 'Can\'t be longer than 150 characters'
        self.fields['lname'].help_text = 'Can\'t be longer than 150 characters'
        self.fields['email'].help_text = 'Enter unique email that contains @'

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data['fname']
        user.last_name = self.cleaned_data['lname']

        if User.objects.filter(email__exact=user.email):
            raise forms.ValidationError('Email already exists')

        if commit:
            user.save()
            return user


class Updateuserform(forms.ModelForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        exclude = ['password1', 'password2']
