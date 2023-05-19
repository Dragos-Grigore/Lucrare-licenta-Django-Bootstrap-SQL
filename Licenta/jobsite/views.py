from django.shortcuts import render, redirect
from jobsite.forms import UserForm,LoginForm,HumanForm
from .models import User
from django.conf import settings
from django.core.mail import send_mail


def say_hello(request):
    mydata = User.objects.all()
    context = {
        'mymembers': mydata,
        'name': 'Johnule'
    }
    return render(request, 'hello.html', context=context)



def sign_up(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['type']
            subject = 'welcome to GFG world'
            message = f'Hi  thank you for registering in geeksforgeeks.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail( subject, message, email_from, recipient_list )
            request.session['email'] = email # set 'token' in the session

            # create a new user object and save it to the database
            user = User(email=email, password=password, type=user_type)
            user.save()
            
            return redirect('human_profile')
    else:
        form = UserForm()
    return render(request, 'sign_up.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            return redirect('main_page')
    else:
        form = LoginForm()
    return render(request, 'log.html',{'form': form})

def human_profile(request):
    if request.method == 'POST':
        form = HumanForm(request.POST)
        if form.is_valid():
            email=request.session['email'] # set 'token' in the session
            full_name = form.cleaned_data.get("full_name")
            phone_number = form.cleaned_data.get("phone_number")
            education = form.cleaned_data.get("phone_number")
            experience = form.cleaned_data.get("experience")
            skills = form.cleaned_data.get("skills")
            hobbies = form.cleaned_data.get("hobbies")
            foreign_languages = form.cleaned_data.get("foreign_languages")
            # create a new user object and save it to the database
            user = User(email=email, full_name=full_name,phone_number=phone_number,education=education,experience=experience,skills=skills,hobbies=hobbies,foreign_languages=foreign_languages )
            user.save()
            
            return redirect('success')
    else:
        form = HumanForm()
    return render(request, 'human_profile.html', {'form': form})

def success(request):
    email=request.session['email'] # set 'token' in the session
    context = {
        'name': email
    }
    return render(request, 'success.html',context=context)

def main_page(request):
    return render(request, 'main_page.html')

