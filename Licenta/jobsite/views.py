from django.http import HttpResponse
from django.shortcuts import render, redirect
from jobsite.forms import UserForm,LoginForm
from .models import User
from django.template import loader
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model

User = get_user_model()

def say_hello(request):
    mydata = User.objects.all()
    template = loader.get_template('hello.html')
    context = {
        'mymembers': mydata,
        'name': 'Johnule'
    }
    return render(request, 'hello.html', context=context)



def sign_up(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['type']
            subject = 'welcome to GFG world'
            message = f'Hi {full_name}, thank you for registering in geeksforgeeks.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail( subject, message, email_from, recipient_list )

            # create a new user object and save it to the database
            user = User(full_name=full_name, email=email, password=password, type=user_type)
            user.save()
            
            return redirect('success')
    else:
        form = UserForm()
        
        
    return render(request, 'sign_up.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    # Authentication successful, log the user in
                    login(request, user)
                    return redirect('main_page')
                else:
                    form.add_error(None, 'Invalid email or password')
            except User.DoesNotExist:
                form.add_error(None, 'Invalid email or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def success(request):
    return render(request, 'success.html')

def main_page(request):
    return render(request, 'main_page.html')

