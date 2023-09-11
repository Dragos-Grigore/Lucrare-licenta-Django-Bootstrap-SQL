from django import forms
from .models import User,Company,Ad
from django.db import connection
from captcha.fields import CaptchaField
from django.contrib.auth.hashers import check_password



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
        if 'Admin' in password or 'admin' in password:
            self.add_error('password', "Password can't contain Admin,admin")
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
            self.add_error('email', "Email doesn't exist")
        if User.objects.filter(email=email).exists():
            user_data = User.objects.filter(email=email).first()
            if 'Admin' in password and password!=user_data.password:
                self.add_error('email', 'Wrong password')
            elif 'Admin' not in password and check_password(password,user_data.password)==False:
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
    code = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter the code from email"}))
  
    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get("code")

        if not code:
            self.add_error('code', 'Complete the code field')


class HumanForm(forms.Form):
    full_name = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter your full name"}))
    phone_number = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter your phone number"}))
    education = forms.CharField(required=False,widget=forms.Textarea(attrs={"placeholder":"Enter your education"}))
    experience = forms.CharField(required=False,widget=forms.Textarea(attrs={"placeholder":"Enter your experience"}))
    skills = forms.CharField(required=False,widget=forms.Textarea(attrs={"placeholder":"Enter your skills"}))
    hobbies = forms.CharField(required=False,widget=forms.Textarea(attrs={"placeholder":"Enter your hobbies"}))
    foreign_languages = forms.CharField(required=False,widget=forms.Textarea(attrs={"placeholder":"Enter your foreign languages"}))

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
            self.add_error('full_name', 'Complete the full name field')
        if len(full_name.split())<2:
            self.add_error('full_name', 'You must have at least two names')
        if  not phone_number:
            self.add_error('full_name', 'Complete the phone number field')
        if phone_number:
            if not phone_number.startswith('0') or len(phone_number) != 10:
                self.add_error('phone_number','Invalid phone number. Phone number should start with 0 and have exactly 10 characters.')
        
        return cleaned_data
    
class CompanyForm(forms.Form):
    company_name = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter your company name"}))
    industry = forms.ChoiceField(choices=[
    ('Unspecified', 'Select an industry'),
    ('Administration', 'Administration'),
    ('Agricultural', 'Agricultural'),
    ('Arts/Entertainment', 'Arts/Entertainment'),
    ('Banks/Financial services', 'Banks/Financial services'),
    ('Call center', 'Call center'),
    ('Chemical', 'Chemical'),
    ('Construction', 'Construction'),
    ('Education', 'Education'),
    ('Food', 'Food'),
    ('Insurance', 'Insurance'),
    ('Manufacturing', 'Manufacturing'),
    ('Marketing/Advertising', 'Marketing/Advertising'),
    ('Media/Communication', 'Media/Communication'),
    ('Medical/Healthcare', 'Medical/Healthcare'),
    ('Oil/Gas/Energy', 'Oil/Gas/Energy'),
    ('Real Estate', 'Real Estate'),
    ('Research/Development', 'Research/Development'),
    ('Technology/IT', 'Technology/IT'),
    ('Telecommunications', 'Telecommunications'),
    ('Transportation', 'Transportation'),
    ('Travel/Hospitality', 'Travel/Hospitality'),
    ('Utilities', 'Utilities'),
    ('Wholesale', 'Wholesale'),
    ('Other', 'Other')
])
    phone_number = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter your phone number"}))
    description = forms.CharField(required=False,widget=forms.Textarea(attrs={"placeholder":"Enter a description"}))


    def clean(self):
        
        cleaned_data = super().clean()
        company_name = cleaned_data.get("company_name")
        industry = cleaned_data.get("industry")
        phone_number = cleaned_data.get("phone_number")
        description = cleaned_data.get("description")

        if  not company_name:
            self.add_error('company_name', 'Complete the company name field')
        if  industry=='Unspecified':
            self.add_error('industry', 'Complete the industry field')
        if  not phone_number:
            self.add_error('phone_number', 'Complete the phone number field')
        if  not description:
            self.add_error('description', 'Complete the description field')
        if phone_number:
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
            self.add_error('email', 'No account using this email')

        return cleaned_data
    
class Change_passForm(forms.Form):
    code = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter the code from email"}))
    password = forms.CharField(required=False,widget=forms.PasswordInput(attrs={"placeholder":"Enter your password"}))
    confirm_password = forms.CharField(required=False,widget=forms.PasswordInput(attrs={"placeholder":"Re-enter your password"}))


    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get("code")
        password= cleaned_data.get("password")
        confirm_password= cleaned_data.get("confirm_password")
        if  not code:
            self.add_error('code', 'Complete the email field')
        if  not password:
            self.add_error('password', 'Complete the password field')
        if  not confirm_password:
            self.add_error('confirm_password', 'Complete the confirm password field')
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
    phone_number = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter your phone number"}))
    job_title = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter a job title"}))
    job_description = forms.CharField(required=False,widget=forms.Textarea(attrs={"placeholder":"Enter a job description"}))
    job_location = forms.ChoiceField(choices=[
    ('Unspecified','Select a location'),
    ('Adelaide', 'Adelaide'),
    ('Amsterdam', 'Amsterdam'),
    ('Athens', 'Athens'),
    ('Auckland', 'Auckland'),
    ('Bangkok', 'Bangkok'),
    ('Barcelona', 'Barcelona'),
    ('Beijing', 'Beijing'),
    ('Berlin', 'Berlin'),
    ('Brussels', 'Brussels'),
    ('Bucharest', 'Bucharest'),
    ('Budapest', 'Budapest'),
    ('Cairo', 'Cairo'),
    ('Cape Town', 'Cape Town'),
    ('Copenhagen', 'Copenhagen'),
    ('Craiova', 'Craiova'),
    ('Dubai', 'Dubai'),
    ('Dublin', 'Dublin'),
    ('Hanoi', 'Hanoi'),
    ('Helsinki', 'Helsinki'),
    ('Iași', 'Iași'),
    ('Jerusalem', 'Jerusalem'),
    ('Lisbon', 'Lisbon'),
    ('London', 'London'),
    ('Los Angeles', 'Los Angeles'),
    ('Melbourne', 'Melbourne'),
    ('Mexico City', 'Mexico City'),
    ('Moscow', 'Moscow'),
    ('Mumbai', 'Mumbai'),
    ('Munich', 'Munich'),
    ('New York', 'New York'),
    ('Oslo', 'Oslo'),
    ('Paris', 'Paris'),
    ('Perth', 'Perth'),
    ('Prague', 'Prague'),
    ('Rio de Janeiro', 'Rio de Janeiro'),
    ('Rome', 'Rome'),
    ('Seoul', 'Seoul'),
    ('Seville', 'Seville'),
    ('Shanghai', 'Shanghai'),
    ('Stockholm', 'Stockholm'),
    ('Sydney', 'Sydney'),
    ('Timișoara', 'Timișoara'),
    ('Tokyo', 'Tokyo'),
    ('Toronto', 'Toronto'),
    ('Vienna', 'Vienna'),
    ('Warsaw', 'Warsaw'),
    ('Wellington', 'Wellington'),
    ('Zurich', 'Zurich'),
    ('Other', 'Other')
])
    department = forms.ChoiceField(choices=[
    ('Unspecified','Select a department'),
    ('Administration', 'Administration'),
    ('Business Development', 'Business Development'),
    ('Consulting', 'Consulting'),
    ('Customer Service', 'Customer Service'),
    ('Data Analytics', 'Data Analytics'),
    ('Finance', 'Finance'),
    ('Human Resources', 'Human Resources'),
    ('IT Hardware', 'IT Hardware'),
    ('IT Software', 'IT Software'),
    ('Legal', 'Legal'),
    ('Marketing', 'Marketing'),
    ('Operations', 'Operations'),
    ('Product Management', 'Product Management'),
    ('Project Management', 'Project Management'),
    ('Public Relations', 'Public Relations'),
    ('Purchasing', 'Purchasing'),
    ('Quality Assurance', 'Quality Assurance'),
    ('Research and Development', 'Research and Development'),
    ('Risk Management', 'Risk Management'),
    ('Sales', 'Sales'),
    ('Supply Chain and Logistics', 'Supply Chain and Logistics'),
    ('Training and Development', 'Training and Development'),
    ('Other', 'Other')
])
    job_type = forms.ChoiceField(choices=[
    ('Unspecified','Select a job type'),
    ('Full time', 'Full time'),
    ('Part time', 'Part time'),
    ('Internship', 'Internship'),
    ('Temporary', 'Temporary')
])
    study_level = forms.ChoiceField(choices=[
    ('Unspecified','Select your study level'),
    ('Unqualified', 'Unqualified'),
    ('Student', 'Student'),
    ('Graduate', 'Graduate')
])
    career_level = forms.ChoiceField(choices=[
    ('Unspecified','Select your study level'),
    ('No experience', 'No experience'),
    ('Entry-Level(< 2 years)', 'Entry-Level(< 2 years)'),
    ('Mid-Level(2-5 years)', 'Mid-Level(2-5 years)'),
    ('Senior-Level(> 5 years)', 'Senior-Level(> 5 years)'),
])
    salary = forms.CharField(required=False,widget=forms.TextInput(attrs={"placeholder":"Enter a salary(€)"}))

    def clean(self):
        cleaned_data = super().clean()
        phone_number= cleaned_data.get("phone_number")
        job_title= cleaned_data.get("job_title")
        job_description = cleaned_data.get("job_description")
        job_location=cleaned_data.get("job_location")
        department=cleaned_data.get("department")
        job_type=cleaned_data.get("job_type")
        study_level=cleaned_data.get("study_level")
        career_level=cleaned_data.get("career_level")
        salary= cleaned_data.get("salary")

        if  not phone_number:
            self.add_error('phone_number', 'Complete the phone number field')
        if  not job_title:
            self.add_error('job_title', 'Complete the job title field')
        if  not job_description:
            self.add_error('job_description', 'Complete the job description field')
        if job_location=='Unspecified':
            self.add_error('job_location','Complete the job location field')
        if department=='Unspecified':
            self.add_error('department','Complete the department field')
        if job_type=='Unspecified':
            self.add_error('job_type','Complete the job type field')
        if study_level=='Unspecified':
            self.add_error('study_level','Complete the study level field')
        if career_level=='Unspecified':
            self.add_error('career_level','Complete the career level field')
        if phone_number:
            if not phone_number.startswith('0') or len(phone_number) != 10:
                self.add_error('phone_number','Invalid phone number. Phone number should start with 0 and have exactly 10 characters.')
        else:
            self.add_error('phone_number','Complete the phone number field')

        return cleaned_data

    def save(self):
        company_id = self.cleaned_data['company_id']
        company_name = self.cleaned_data['company_name']
        industry = self.cleaned_data['industry']
        phone_number=self.cleaned_data['phone_number']
        job_title=self.cleaned_data['job_title']
        job_description=self.cleaned_data['job_description']
        job_location = self.cleaned_data['job_location']
        department=self.cleaned_data['department']
        job_type=self.cleaned_data['job_type']
        study_level=self.cleaned_data['study_level']
        career_level=self.cleaned_data['career_level']
        salary=self.cleaned_data['salary']
        posted_date = self.cleaned_data['posted_date']
        cursor = connection.cursor()
        cursor.execute("INSERT INTO jobsite_ad (company_id, company_name, industry, phone_number, job_title, job_description,job_location,department, job_type,study_level,career_level, salary, posted_date) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s,%s,%s, %s, %s)", [company_id, company_name, industry, phone_number, job_title, job_description,job_location,department, job_type,study_level,career_level, salary, posted_date])
        connection.commit()
        connection.close()

class SearchBarForm(forms.Form):
    searchBar= forms.CharField(required=False,widget=forms.TextInput)
    job_location = forms.ChoiceField(choices=[
    ('Unspecified','Select a location'),
    ('Adelaide', 'Adelaide'),
    ('Amsterdam', 'Amsterdam'),
    ('Athens', 'Athens'),
    ('Auckland', 'Auckland'),
    ('Bangkok', 'Bangkok'),
    ('Barcelona', 'Barcelona'),
    ('Beijing', 'Beijing'),
    ('Berlin', 'Berlin'),
    ('Brussels', 'Brussels'),
    ('Bucharest', 'Bucharest'),
    ('Budapest', 'Budapest'),
    ('Cairo', 'Cairo'),
    ('Cape Town', 'Cape Town'),
    ('Copenhagen', 'Copenhagen'),
    ('Craiova', 'Craiova'),
    ('Dubai', 'Dubai'),
    ('Dublin', 'Dublin'),
    ('Hanoi', 'Hanoi'),
    ('Helsinki', 'Helsinki'),
    ('Iași', 'Iași'),
    ('Jerusalem', 'Jerusalem'),
    ('Lisbon', 'Lisbon'),
    ('London', 'London'),
    ('Los Angeles', 'Los Angeles'),
    ('Melbourne', 'Melbourne'),
    ('Mexico City', 'Mexico City'),
    ('Moscow', 'Moscow'),
    ('Mumbai', 'Mumbai'),
    ('Munich', 'Munich'),
    ('New York', 'New York'),
    ('Oslo', 'Oslo'),
    ('Paris', 'Paris'),
    ('Perth', 'Perth'),
    ('Prague', 'Prague'),
    ('Rio de Janeiro', 'Rio de Janeiro'),
    ('Rome', 'Rome'),
    ('Seoul', 'Seoul'),
    ('Seville', 'Seville'),
    ('Shanghai', 'Shanghai'),
    ('Stockholm', 'Stockholm'),
    ('Sydney', 'Sydney'),
    ('Timișoara', 'Timișoara'),
    ('Tokyo', 'Tokyo'),
    ('Toronto', 'Toronto'),
    ('Vienna', 'Vienna'),
    ('Warsaw', 'Warsaw'),
    ('Wellington', 'Wellington'),
    ('Zurich', 'Zurich'),
    ('Other', 'Other')
])
    department = forms.ChoiceField(choices=[
    ('Unspecified','Select a department'),
    ('Administration', 'Administration'),
    ('Business Development', 'Business Development'),
    ('Consulting', 'Consulting'),
    ('Customer Service', 'Customer Service'),
    ('Data Analytics', 'Data Analytics'),
    ('Finance', 'Finance'),
    ('Human Resources', 'Human Resources'),
    ('IT Hardware', 'IT Hardware'),
    ('IT Software', 'IT Software'),
    ('Legal', 'Legal'),
    ('Marketing', 'Marketing'),
    ('Operations', 'Operations'),
    ('Product Management', 'Product Management'),
    ('Project Management', 'Project Management'),
    ('Public Relations', 'Public Relations'),
    ('Purchasing', 'Purchasing'),
    ('Quality Assurance', 'Quality Assurance'),
    ('Research and Development', 'Research and Development'),
    ('Risk Management', 'Risk Management'),
    ('Sales', 'Sales'),
    ('Supply Chain and Logistics', 'Supply Chain and Logistics'),
    ('Training and Development', 'Training and Development'),
    ('Other', 'Other')
])
    job_type = forms.ChoiceField(choices=[
    ('Unspecified','Select a job type'),
    ('Full time', 'Full time'),
    ('Part time', 'Part time'),
    ('Internship', 'Internship'),
    ('Temporary', 'Temporary')
])
    study_level = forms.ChoiceField(choices=[
    ('Unspecified','Select your study level'),
    ('Unqualified', 'Unqualified'),
    ('Student', 'Student'),
    ('Graduate', 'Graduate')
])
    career_level = forms.ChoiceField(choices=[
    ('Unspecified','Select your career level'),
    ('No experience', 'No experience'),
    ('Entry-Level(< 2 years)', 'Entry-Level(< 2 years)'),
    ('Mid-Level(2-5 years)', 'Mid-Level(2-5 years)'),
    ('Senior-Level(> 5 years)', 'Senior-Level(> 5 years)'),
])
    industry = forms.ChoiceField(choices=[
    ('Unspecified', 'Select an industry'),
    ('Administration', 'Administration'),
    ('Agricultural', 'Agricultural'),
    ('Arts/Entertainment', 'Arts/Entertainment'),
    ('Banks/Financial services', 'Banks/Financial services'),
    ('Call center', 'Call center'),
    ('Chemical', 'Chemical'),
    ('Construction', 'Construction'),
    ('Education', 'Education'),
    ('Food', 'Food'),
    ('Insurance', 'Insurance'),
    ('Manufacturing', 'Manufacturing'),
    ('Marketing/Advertising', 'Marketing/Advertising'),
    ('Media/Communication', 'Media/Communication'),
    ('Medical/Healthcare', 'Medical/Healthcare'),
    ('Oil/Gas/Energy', 'Oil/Gas/Energy'),
    ('Real Estate', 'Real Estate'),
    ('Research/Development', 'Research/Development'),
    ('Technology/IT', 'Technology/IT'),
    ('Telecommunications', 'Telecommunications'),
    ('Transportation', 'Transportation'),
    ('Travel/Hospitality', 'Travel/Hospitality'),
    ('Utilities', 'Utilities'),
    ('Wholesale', 'Wholesale'),
    ('Other', 'Other')
])
    
    def clean(self):
        cleaned_data = super().clean()
        searchBar = cleaned_data.get("searchBar")

class MiniSearchForm(forms.Form):
    searchBar= forms.CharField(widget=forms.TextInput)

    def clean(self):
        cleaned_data = super().clean()
        searchBar = cleaned_data.get("searchBar")


