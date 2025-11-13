from django import forms
from django.contrib.auth.models import User
from .models import Profile

# -------------------------------
# Login Form
# -------------------------------
class LoginForm(forms.Form):
    """
    Simple login form for user authentication using username and password.
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)  # Hide input

# -------------------------------
# User Registration Form
# -------------------------------
class UserRegistrationForm(forms.ModelForm):
    """
    Form for registering a new user.

    Fields:
        username, first_name, email, password, password2 (confirmation)
    """
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        """
        Validate that password and password2 match.
        """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match')
        return cd['password2']

    def clean_email(self):
        """
        Ensure the email is unique in the database.
        """
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Email already in use.")
        return data

# -------------------------------
# User Edit Form
# -------------------------------
class UserEditForm(forms.ModelForm):
    """
    Form for editing existing user's basic info: first_name, last_name, email.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        """
        Ensure the updated email is unique (excluding current user).
        """
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email already in use')
        return data

# -------------------------------
# Profile Edit Form
# -------------------------------
class ProfileEditForm(forms.ModelForm):
    """
    Form for editing Profile model fields: date_of_birth, photo.
    """
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
