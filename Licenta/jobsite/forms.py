from django import forms
from .models import User
from django.db import connection
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter your full name"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder":"Enter your email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Enter your password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Re-enter your password"}))
    type = forms.ChoiceField(choices=[('human', 'Human'), ('company', 'Company')])
    captcha = CaptchaField()


    def clean(self):
        
        cleaned_data = super().clean()
        full_name = cleaned_data.get("full_name")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if  not full_name:
            self.add_error('full_name', 'Complete the full name field')
        if  not email:
            self.add_error('email', 'Complete the email field')
        if  not password:
            self.add_error('password', 'Complete the password field')
        if  not confirm_password:
            self.add_error('confirm_password', 'Complete the confirm password field')
        if len(full_name.split())<2:
            self.add_error('full_name', 'You must have at least two names')
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Email already used')
        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')
        if len(password)<8:
            self.add_error('password', 'Password is to short')
        if len(password)>40:
            self.add_error('password', 'Password is to long')
        upper=False
        lower=False
        digit=False
        for char in password:
            if char.isupper():
                upper=True
            if char.islower():
                lower=True
            if char.isdigit():
                digit=True
        if upper==False or lower==False or digit==False:
            self.add_error('password', 'Password should have at least one A-Z, a-z, 0-9')
        return cleaned_data

    
    def save(self):
        full_name = self.cleaned_data['full_name']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        type = self.cleaned_data['type']
        cursor = connection.cursor()
        cursor.execute("INSERT INTO jobsite_user (full_name, email, password, type) VALUES (%s, %s, %s, %s)", [full_name, email, password, type])
        connection.commit()

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email',widget=forms.TextInput(attrs={"placeholder":"Enter your email"}))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={"placeholder":"Enter your password"}))

    def clean(self):
        
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if  not email:
            self.add_error('email', 'Complete the email field')
        if  not password:
            self.add_error('password', 'Complete the password field')
        return cleaned_data
