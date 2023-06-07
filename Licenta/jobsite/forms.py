from django import forms
from .models import User,Company,Ad
from django.db import connection
from captcha.fields import CaptchaField
from .rsa_utils import RSAUtils
from django.contrib.auth.hashers import check_password
from datetime import date


# Instantiate RSAUtils class

class UserForm(forms.Form):
    email = forms.EmailField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter your email"}))
    password = forms.CharField(required=False,widget=forms.PasswordInput(attrs={"placeholder":"Enter your password"}))
    confirm_password = forms.CharField(required=False,widget=forms.PasswordInput(attrs={"placeholder":"Re-enter your password"}))
    type = forms.ChoiceField(choices=[('Human','Human'), ('Company','Company')])
    captcha = CaptchaField(required=False)


    def clean(self):
        
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        captcha= cleaned_data.get("captcha")
        if  not email:
            self.add_error('email', 'Complete the email field')
        if  not password:
            self.add_error('password', 'Complete the password field')
        if  not confirm_password:
            self.add_error('confirm_password', 'Complete the confirm password field')
        if  not captcha:
            self.add_error('captcha', 'Complete the captcha field')
        if User.objects.filter(email=email).exists() or Company.objects.filter(email=email).exists():
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
        if type=='Human':
            cursor.execute("INSERT INTO jobsite_user (email, password, type) VALUES (%s, %s, %s)", [ email, password, type])
        if type=='Company':
            cursor.execute("INSERT INTO jobsite_company (email, password, type) VALUES (%s, %s, %s)", [ email, password, type])
        connection.commit()
        connection.close()

class LoginForm(forms.Form):
    email = forms.EmailField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter your email"}))
    password = forms.CharField(required=False,widget=forms.PasswordInput(attrs={"placeholder":"Enter your password"}))

    def clean(self):
        
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if  not email:
            self.add_error('email', 'Complete the email field')
        if  not password:
            self.add_error('password', 'Complete the password field')
        if not User.objects.filter(email=email).exists() and not Company.objects.filter(email=email).exists():
            self.add_error('email', 'Email doesnt exist')
        if User.objects.filter(email=email).exists():
            user_data = User.objects.filter(email=email).first()
            if check_password(password,user_data.password)==False:
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
        elif Company.objects.filter(email=email).exists():
            user_data = Company.objects.filter(email=email).first()
            if check_password(password,user_data.password)==False:
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

class log2FAForm(forms.Form):
    code = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter your password"}))
  
    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get("code")

        if not code:
            self.add_error('code', 'Complete the email field')


class HumanForm(forms.Form):
    full_name = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter your full name"}))
    phone_number = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter your phone number"}))
    education = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Re-enter your education"}))
    experience = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Re-enter your experience"}))
    skills = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter your skills"}))
    hobbies = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter your hobbies"}))
    foreign_languages = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter your language"}))

    def clean(self):
        
        cleaned_data = super().clean()
        full_name = cleaned_data.get("full_name")
        phone_number = cleaned_data.get("phone_number")
        education = cleaned_data.get("education")
        experience = cleaned_data.get("experience")
        skills = cleaned_data.get("skills")
        hobbies = cleaned_data.get("hobbies")
        foreign_languages = cleaned_data.get("foreign_languages")

        if  not full_name:
            self.add_error('full_name', 'Complete the email field')
        if len(full_name.split())<2:
            self.add_error('full_name', 'You must have at least two names')
        if  not phone_number:
            self.add_error('full_name', 'Complete the email field')
        if phone_number:
            # Check if phone_number starts with '0' and has exactly 10 characters
            if not phone_number.startswith('0') or len(phone_number) != 10:
                self.add_error('phone_number','Invalid phone number. Phone number should start with 0 and have exactly 10 characters.')
        
        return cleaned_data
    
class CompanyForm(forms.Form):
    company_name = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter your company name"}))
    industry = forms.ChoiceField(choices=[
    ('Unspecified','Select a location'),
    ('Administration', 'Administration'),
    ('Agricultural', 'Agricultural'),
    ('Food', 'Food'),
    ('Arts/Entertainment', 'Arts/Entertainment'),
    ('Insurance', 'Insurance'),
    ('Other', 'Other')
])
    phone_number = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Re-enter your phone number"}))
    description = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Re-enter your description"}))


    def clean(self):
        
        cleaned_data = super().clean()
        company_name = cleaned_data.get("company_name")
        industry = cleaned_data.get("industry")
        phone_number = cleaned_data.get("phone_number")
        description = cleaned_data.get("description")

        if  not company_name:
            self.add_error('company_name', 'Complete the email field')
        if  industry=='Unspecified':
            self.add_error('industry', 'Complete the email field')
        if  not phone_number:
            self.add_error('phone_number', 'Complete the email field')
        if  not description:
            self.add_error('description', 'Complete the email field')
        if phone_number:
            # Check if phone_number starts with '0' and has exactly 10 characters
            if not phone_number.startswith('0') or len(phone_number) != 10:
                self.add_error('phone_number','Invalid phone number. Phone number should start with 0 and have exactly 10 characters.')

        return cleaned_data

class Forgot_passForm(forms.Form):
    email = forms.EmailField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter your email"}))

    def clean(self):
        
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        if  not email:
            self.add_error('email', 'Complete the email field')
        if not User.objects.filter(email=email).exists() and not Company.objects.filter(email=email).exists():
            self.add_error('email', 'Email already used')

        return cleaned_data
    
class Change_passForm(forms.Form):
    code = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter your password"}))
    password = forms.CharField(required=False,widget=forms.PasswordInput(attrs={"placeholder":"Enter your password"}))
    confirm_password = forms.CharField(required=False,widget=forms.PasswordInput(attrs={"placeholder":"Enter your password"}))


    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get("code")
        password= cleaned_data.get("password")
        confirm_password= cleaned_data.get("confirm_password")
        if  not code:
            self.add_error('code', 'Complete the email field')
        if  not password:
            self.add_error('password', 'Complete the email field')
        if  not confirm_password:
            self.add_error('confirm_password', 'Complete the email field')
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
    
class AdForm(forms.Form):
    phone_number = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter your password"}))
    job_title = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter your password"}))
    job_description = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter your password"}))
    job_location = forms.ChoiceField(choices=[
    ('location','Select a location'),
    ('New York', 'New York'),
    ('San Francisco', 'San Francisco'),
    ('London', 'London'),
    ('Tokyo', 'Toyo'),
    ('Paris', 'Paris'),
    ('Berlin', 'Berlin'),
    ('Sydney', 'Sydney'),
    ('Mumbai', 'Mumbai'),
    ('Toronto', 'Toronto'),
    ('Dubai', 'Dubai'),
])
    department = forms.ChoiceField(choices=[
    ('unspecified','Select a location'),
    ('New York', 'New York'),
    ('San Francisco', 'San Francisco'),
    ('London', 'London'),
    ('Tokyo', 'Tokyo'),
    ('Paris', 'Paris'),
    ('Berlin', 'Berlin'),
    ('Sydney', 'Sydney'),
    ('Mumbai', 'Mumbai'),
    ('Toronto', 'Toronto'),
    ('Dubai', 'Dubai'),
    ('Other', 'Other')
])
    job_type = forms.ChoiceField(choices=[
    ('unspecified','Select a job_type'),
    ('Full time', 'Full time'),
    ('Part time', 'Part time'),
    ('Internship', 'Internship'),
    ('Temporary', 'Temporary')
])
    study_level = forms.ChoiceField(choices=[
    ('Unspecified','Select a your study_level'),
    ('Unqualified', 'Unqualified'),
    ('Student', 'Student'),
    ('Graduate', 'Graduate')
])
    career_level = forms.ChoiceField(choices=[
    ('Unspecified','Select a your study_level'),
    ('No experience', 'No experience'),
    ('Entry-Level(< 2 years)', 'Entry-Level(< 2 years)'),
    ('Mid-Level(2-5 years)', 'Mid-Level(2-5 years)'),
    ('Senior-Level(> 5 years)', 'Senior-Level(> 5 years)'),
])
    salary = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter your password"}))

    def clean(self):
        cleaned_data = super().clean()
        phone_number= cleaned_data.get("phone_number")
        job_title= cleaned_data.get("job_title")
        job_description = cleaned_data.get("job_description")
        job_location=cleaned_data.get("job_location")
        salary= cleaned_data.get("salary")

        if  not phone_number:
            self.add_error('phone_number', 'Complete the email field')
        if  not job_title:
            self.add_error('job_title', 'Complete the email field')
        if  not job_description:
            self.add_error('job_description', 'Complete the email field')
        if job_location=='location':
            self.add_error('job_location','Complete')
        if phone_number:
            # Check if phone_number starts with '0' and has exactly 10 characters
            if not phone_number.startswith('0') or len(phone_number) != 10:
                self.add_error('phone_number','Invalid phone number. Phone number should start with 0 and have exactly 10 characters.')
        
        return cleaned_data

    def save(self):
        company_id = self.cleaned_data['company_id']
        company_name = self.cleaned_data['company_name']
        industry = self.cleaned_data['industry']
        phone_number=self.cleaned_data['phone_number']
        job_title=self.cleaned_data['job_title']
        job_description=self.cleaned_data['job_description']
        job_location = self.cleaned_data['job_location']
        salary=self.cleaned_data['salary']
        posted_date = self.cleaned_data['posted_date']
        cursor = connection.cursor()
        cursor.execute("INSERT INTO jobsite_ad (company_id, company_name, industry, phone_number, job_title, job_description,job_location, salary, posted_date) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s)", [company_id, company_name, industry, phone_number, job_title, job_description,job_location, salary, posted_date])
        connection.commit()
        connection.close()

class SearchBarForm(forms.Form):
    searchBar= forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter your password"}))
    job_location = forms.ChoiceField(choices=[
    ('Unspecified','Select a location'),
    ('New York', 'New York'),
    ('San Francisco', 'San Francisco'),
    ('London', 'London'),
    ('Tokyo', 'Toyo'),
    ('Paris', 'Paris'),
    ('Berlin', 'Berlin'),
    ('Sydney', 'Sydney'),
    ('Mumbai', 'Mumbai'),
    ('Toronto', 'Toronto'),
    ('Dubai', 'Dubai'),
])
    department = forms.ChoiceField(choices=[
    ('Unspecified','Select a location'),
    ('New York', 'New York'),
    ('San Francisco', 'San Francisco'),
    ('London', 'London'),
    ('Tokyo', 'Tokyo'),
    ('Paris', 'Paris'),
    ('Berlin', 'Berlin'),
    ('Sydney', 'Sydney'),
    ('Mumbai', 'Mumbai'),
    ('Toronto', 'Toronto'),
    ('Dubai', 'Dubai'),
    ('Other', 'Other')
])
    job_type = forms.ChoiceField(choices=[
    ('Unspecified','Select a job_type'),
    ('Full time', 'Full time'),
    ('Part time', 'Part time'),
    ('Internship', 'Internship'),
    ('Temporary', 'Temporary')
])
    study_level = forms.ChoiceField(choices=[
    ('Unspecified','Select a your study_level'),
    ('Unqualified', 'Unqualified'),
    ('Student', 'Student'),
    ('Graduate', 'Graduate')
])
    career_level = forms.ChoiceField(choices=[
    ('Unspecified','Select a your study_level'),
    ('No experience', 'No experience'),
    ('Entry-Level(< 2 years)', 'Entry-Level(< 2 years)'),
    ('Mid-Level(2-5 years)', 'Mid-Level(2-5 years)'),
    ('Senior-Level(> 5 years)', 'Senior-Level(> 5 years)'),
])
    industry = forms.ChoiceField(choices=[
    ('Unspecified','Select a location'),
    ('Administration', 'Administration'),
    ('Agricultural', 'Agricultural'),
    ('Food', 'Food'),
    ('Arts/Entertainment', 'Arts/Entertainment'),
    ('Insurance', 'Insurance'),
    ('Other', 'Other')
])
    
    def clean(self):
        cleaned_data = super().clean()
        searchBar = cleaned_data.get("searchBar")
