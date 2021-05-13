from django import forms
from django.core.validators import MinValueValidator,MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import date
import requests

def validate_CFUsername(value):
    url = "https://codeforces.com/api/user.rating?handle=" + str(value)
    data = requests.get(url)
    JSONdata = data.json()
    if JSONdata["status"] == 'OK' :
        return value
    else:
        raise ValidationError(
            "codeforces account does not exist, check again"
        )

class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
                                                                    "placeholder"   : "Enter Username",
                                                                    "class"         : "form-control",
                                                                    "id"            : "user-name",
                                                                    "required"      : True ,
                                                                    "autofocus"     : True
                                                                    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
                                                                    "placeholder"   : "Password",
                                                                    "class"         : "form-control",
                                                                    "required"      : True,
                                                                    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
                                                                    "placeholder"   : " Confirm Password",
                                                                    "class"         : "form-control",
                                                                    "required"      : True,
                                                                    }))
    name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={
                                                                    "placeholder"   : "Name",
                                                                    "class"         : "form-control",
                                                                    "required"      : True,
                                                                    }))
    CodeForces_Username = forms.CharField(validators=[validate_CFUsername], max_length=30,widget=forms.TextInput(attrs={
                                                                    "placeholder"   : "Code Forces Username",
                                                                    "class"         : "form-control",
                                                                    "id"            : "name",
                                                                    "required"      : True,
                                                                    }))
    email = forms.EmailField(max_length=254,widget=forms.TextInput(attrs={
                                                                    "placeholder"   : "Email",
                                                                    "class"         : "form-control",
                                                                    "id"            : "email",
                                                                    "required"      : True,
                                                                    }))
    year = forms.IntegerField(validators=[MinValueValidator(2010), MaxValueValidator(date.today().year)],widget=forms.NumberInput(attrs={
                                                                    "placeholder"   : "Year of Admission",
                                                                    "class"         : "form-control",
                                                                    "id"            : "year",
                                                                    "required"      : True,
                                                                    }))
    class Meta:
        model = User
        fields = ('email', 'username', 'name', 'CodeForces_Username','year', 'password1', 'password2', )

