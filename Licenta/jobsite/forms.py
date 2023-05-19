from django import forms
from .models import User
from django.db import connection
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder":"Enter your email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Enter your password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Re-enter your password"}))
    type = forms.ChoiceField(choices=[('human', 'Human'), ('company', 'Company')])
    captcha = CaptchaField()


    def clean(self):
        
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if  not email:
            self.add_error('email', 'Complete the email field')
        if  not password:
            self.add_error('password', 'Complete the password field')
        if  not confirm_password:
            self.add_error('confirm_password', 'Complete the confirm password field')
        #if len(full_name.split())<2:
            #self.add_error('full_name', 'You must have at least two names')
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
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        type = self.cleaned_data['type']
        cursor = connection.cursor()
        if type=='human' or type=='Human':
            cursor.execute("INSERT INTO jobsite_user (email, password, type) VALUES (%s, %s, %s)", [ email, password, type])
        connection.commit()

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder":"Enter your email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Enter your password"}))

    def clean(self):
        
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if  not email:
            self.add_error('email', 'Complete the email field')
        if  not password:
            self.add_error('password', 'Complete the password field')
        if not User.objects.filter(email=email).exists():
            self.add_error('email', 'Email doesnt exist')
        if User.objects.filter(email=email).exists():
            user_data = User.objects.filter(email=email).first()
            if user_data.password!=password:
                self.add_error('email', 'Wrong password')
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
    
class HumanForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter your full name"}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter your phone number"}))
    education = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Re-enter your education"}))
    experience = forms.ChoiceField(widget=forms.TextInput(attrs={"placeholder":"Re-enter your experience"}))
    skills = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter your skills"}))
    hobbies = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter your hobbies"}))
    foreign_languages = forms.ChoiceField(widget=forms.TextInput(attrs={"placeholder":"Enter your language"}))


    def clean(self):
        
        cleaned_data = super().clean()
        full_name = cleaned_data.get("full_name")
        phone_number = cleaned_data.get("phone_number")
        education = cleaned_data.get("phone_number")
        experience = cleaned_data.get("experience")
        skills = cleaned_data.get("skills")
        hobbies = cleaned_data.get("hobbies")
        foreign_languages = cleaned_data.get("foreign_languages")

        return cleaned_data

    
    def save(self):
        email = self.cleaned_data['email']
        full_name = self.cleaned_data.get("full_name")
        phone_number = self.cleaned_data.get("phone_number")
        education = self.cleaned_data.get("phone_number")
        experience = self.cleaned_data.get("experience")
        skills = self.cleaned_data.get("skills")
        hobbies = self.cleaned_data.get("hobbies")
        foreign_languages = self.cleaned_data.get("foreign_languages")
        cursor = connection.cursor()
        cursor.execute("UPDATE user_profile SET full_name = %s, phone_number = %s, education = %s, experience = %s, skills = %s, hobbies = %s, foreign_languages = %s WHERE email = %s", [full_name, phone_number, education, experience, skills, hobbies, foreign_languages, email])
        connection.commit()