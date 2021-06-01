from django import forms
from django.core.validators import MinValueValidator,MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from datetime import date
from .models import UserProfile
from .codeforces_API import getRating,fetchCFProfileInfo


def validate_CFUsername(value):
    if UserProfile.objects.filter(codeForces_username =value).exists():
            raise ValidationError(
                "Username already exists"
            )
    JSONdata = fetchCFProfileInfo(str(value))
    if JSONdata["status"] == {} :
        raise ValidationError(
            "codeforces account does not exist, check again"
        )
    return value
        
    

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
    codeForces_username = forms.CharField(validators=[validate_CFUsername],help_text="need help?", max_length=30,widget=forms.TextInput(attrs={
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
        fields = ('email', 'username', 'name', 'codeForces_username','year', 'password1', 'password2', )
    
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        user_profile = UserProfile.objects.create(user = user,
                                                    name                = self.cleaned_data['name'],
                                                    codeForces_username =self.cleaned_data['codeForces_username'],
                                                    year                = self.cleaned_data['year'],
                                                    rating              = getRating(self.cleaned_data['codeForces_username'])
                                                )

        user_profile.add_solvedProblems()

        return user

class EditProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
                                                                    "placeholder"   : "Enter Username",
                                                                    "class"         : "form-control",
                                                                    "id"            : "user-name",
                                                                    "required"      : True ,
                                                                    "autofocus"     : True
                                                                    }))
    
    name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={
                                                                    "placeholder"   : "Name",
                                                                    "class"         : "form-control",
                                                                    "required"      : True,
                                                                    }))
    codeForces_username = forms.CharField(validators=[validate_CFUsername], max_length=30,widget=forms.TextInput(attrs={
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
        fields = (
            'username',
            'email',
            'name',
            'codeForces_username',
        )
        exclude = ('password1',)

    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        
        UserProfile.objects.filter(user = user).update(
                                            name                = self.cleaned_data['name'],
                                            codeForces_username = self.cleaned_data['codeForces_username'],
                                            year                = self.cleaned_data['year'],
            
                                        )
    
        return user