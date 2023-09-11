from django.shortcuts import render, redirect
from jobsite.forms import UserForm,LoginForm,HumanForm,CompanyForm,Forgot_passForm,Change_passForm,log2FAForm,AdForm,SearchBarForm,MiniSearchForm
from .models import User,Company,Ad,Application
from django.conf import settings
from django.core.mail import send_mail
from django.db import connection
from django.contrib.auth.hashers import make_password
import random
from datetime import date
from django.db.models import Q



def say_hello(request):
    email='None'
    usertype='None'
    request.session['usertype'] = usertype
    request.session['email'] = email

    if request.method == 'POST':
        form = SearchBarForm(request.POST)
        if form.is_valid():
            searchBar = form.cleaned_data.get("searchBar")
            job_location = form.cleaned_data.get("job_location")
            department = form.cleaned_data.get("department")
            job_type = form.cleaned_data.get("job_type")
            study_level = form.cleaned_data.get("study_level")
            career_level = form.cleaned_data.get("career_level")
            industry = form.cleaned_data.get("industry")
            request.session['searchBar'] = searchBar    
            request.session['job_location'] = job_location     
            request.session['department'] = department     
            request.session['job_type'] = job_type 
            request.session['study_level'] = study_level    
            request.session['career_level'] = career_level    
            request.session['industry'] = industry    
            return redirect('show_filtered_ads_not_logged')
    else:
        form = SearchBarForm()
    return render(request, 'hello.html',{'form': form})



def sign_up(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['type']
            coded_password=make_password(password)
            subject = 'Welcome to our new app'
            message = f'Thank you for registering to our app.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail( subject, message, email_from, recipient_list )
            request.session['email'] = email
            if user_type=='human' or user_type=='Human':
                user = User(email=email, password=coded_password, type=user_type)
                user.save()
                return redirect('edit_human_profile')
            elif user_type=='company' or user_type=='Company':
                user = Company(email=email, password=coded_password, type=user_type)
                user.save()
                return redirect('edit_company_profile')
    else:
        form = UserForm()
    return render(request, 'sign_up.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            random_number = random.randint(1000, 9999)
            subject = 'Action Required: Verify Your Identity with 2FA'
            message = f'Your verification code is: {random_number}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail( subject, message, email_from, recipient_list )
            request.session['random_number'] = random_number
            request.session['email'] = email

            return redirect('log2FA')
    else:
        form = LoginForm()
    return render(request, 'log.html',{'form': form})

def log2FA(request):
    random_number=request.session['random_number']
    if request.method == 'POST':
        form = log2FAForm(request.POST)
        if form.is_valid():
            email=request.session['email']
            code=form.cleaned_data['code']
            code = int(code)
            if code != random_number:
                return redirect ('error_log2FA')
            if User.objects.filter(email=email).exists():
                return redirect('main_page_human')
            elif Company.objects.filter(email=email).exists():
                return redirect('main_page_company')
    else:
        form = log2FAForm()
    return render(request, 'log2FA.html',{'form': form})

def error_log2FA(request):
    random_number=request.session['random_number']
    if request.method == 'POST':
        form = log2FAForm(request.POST)
        if form.is_valid():
            email=request.session['email']
            code=form.cleaned_data['code']
            code = int(code)
            if code != random_number:
                return redirect ('error_log2FA')
            elif User.objects.filter(email=email).exists():
                return redirect('main_page_human')
            elif Company.objects.filter(email=email).exists():
                return redirect('main_page_company')
    else:
        form = log2FAForm()
    return render(request, 'error_log2FA.html',{'form': form})


def forgot_pass(request):
        if request.method == 'POST':
            form = Forgot_passForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                random_number = random.randint(1000, 9999)
                subject = 'Reset password'
                message = f'Your code is: {random_number}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email, ]
                send_mail( subject, message, email_from, recipient_list )
                request.session['email'] = email
                request.session['random_number'] = random_number
                return redirect('change_pass')
        else:
            form = Forgot_passForm()
        return render(request, 'forgot_pass.html',{'form': form})

def change_pass(request):
    random_number=request.session.get('random_number')
    if request.method == 'POST':
        form = Change_passForm(request.POST)
        if form.is_valid():
            email=request.session['email']
            password=form.cleaned_data['password']
            code=form.cleaned_data['code']
            code = int(code)
            if code != random_number:
                return redirect ('error_change_pass')
            else:
                cursor = connection.cursor()
                coded_password=make_password(password)
                if User.objects.filter(email=email).exists(): 
                    cursor.execute("UPDATE jobsite_user SET password = %s WHERE email = %s", [coded_password, email])
                elif Company.objects.filter(email=email).exists():
                    cursor.execute("UPDATE jobsite_company SET password = %s WHERE email = %s", [coded_password, email])
                connection.commit()
                connection.close()    
                return redirect('log')
    else:
        form = Change_passForm()
    return render(request, 'change_pass.html',{'form': form})

def error_change_pass(request):
    random_number=request.session.get('random_number')
    if request.method == 'POST':
        form = Change_passForm(request.POST)
        if form.is_valid():
            email=request.session['email']
            password=form.cleaned_data['password']
            code=form.cleaned_data['code']
            code = int(code)
            if code != random_number:
                return redirect ('error_change_pass')
            else:
                cursor = connection.cursor()
                coded_password=make_password(password)
                if User.objects.filter(email=email).exists(): 
                    cursor.execute("UPDATE jobsite_user SET password = %s WHERE email = %s", [coded_password, email])
                elif Company.objects.filter(email=email).exists():
                    cursor.execute("UPDATE jobsite_company SET password = %s WHERE email = %s", [coded_password, email])
                connection.commit()
                connection.close()    
                return redirect('log')
    else:
        form = Change_passForm()
    return render(request, 'error_change_pass.html',{'form': form})


def edit_human_profile(request):
    email=request.session['email']
    user_data = User.objects.filter(email=email).first()
    if request.method == 'POST':
        form = HumanForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data.get("full_name")
            if full_name is None:
                full_name='unspecified'
            phone_number = form.cleaned_data.get("phone_number")
            if phone_number is None:
                phone_number='unspecified'
            education = form.cleaned_data.get("education")
            if education is None:
                education='unspecified'
            experience = form.cleaned_data.get("experience")
            if experience is None:
                experience='unspecified'            
            skills = form.cleaned_data.get("skills")
            if skills is None:
                skills='unspecified'
            hobbies = form.cleaned_data.get("hobbies")
            if hobbies is None:
                hobbies='unspecified'
            foreign_languages = form.cleaned_data.get("foreign_languages")
            if foreign_languages is None:
                foreign_languages='unspecified'

            cursor = connection.cursor()
            cursor.execute("UPDATE jobsite_user SET full_name = %s, phone_number = %s, education = %s, experience = %s, skills = %s, hobbies = %s, foreign_languages = %s WHERE email = %s", [full_name, phone_number, education, experience, skills, hobbies, foreign_languages, email])
            connection.commit()
            connection.close()
            
            return redirect('main_page_human')
    else:
        initial_data = {}

        if user_data.full_name != 'unspecified':
            initial_data['full_name'] = user_data.full_name

        if user_data.phone_number != 'unspecified':
            initial_data['phone_number'] = user_data.phone_number

        if user_data.education != 'unspecified':
            initial_data['education'] = user_data.education

        if user_data.experience != 'unspecified':
            initial_data['experience'] = user_data.experience

        if user_data.skills != 'unspecified':
            initial_data['skills'] = user_data.skills

        if user_data.hobbies != 'unspecified':
            initial_data['hobbies'] = user_data.hobbies

        if user_data.foreign_languages  != 'unspecified':
            initial_data['foreign_languages'] = user_data.foreign_languages 

        form = HumanForm(initial=initial_data)    
    return render(request, 'edit_human_profile.html', {'form': form})

def edit_company_profile(request):
    email=request.session['email']
    user_data = Company.objects.filter(email=email).first()
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data.get("company_name")
            if company_name is None:
                company_name='unspecified'
            industry = form.cleaned_data.get("industry")
            if industry is None:
                industry='unspecified'
            phone_number = form.cleaned_data.get("phone_number")
            if phone_number is None:
                phone_number='unspecified'
            description = form.cleaned_data.get("description")
            if description is None:
                description='unspecified'            
            cursor = connection.cursor()
            cursor.execute("UPDATE jobsite_company SET company_name = %s, industry = %s, phone_number = %s, description = %s WHERE email = %s", [company_name,industry, phone_number, description, email])
            connection.commit()
            connection.close()
            
            return redirect('main_page_company')
    else:
        initial_data = {}
    
        if user_data.company_name != 'unspecified':
            initial_data['company_name'] = user_data.company_name

        if user_data.industry != 'unspecified':
            initial_data['industry'] = user_data.industry

        if user_data.phone_number != 'unspecified':
            initial_data['phone_number'] = user_data.phone_number

        if user_data.description != 'unspecified':
            initial_data['description'] = user_data.description
 
        form = CompanyForm(initial={'company_name':user_data.company_name,'industry':user_data.industry,'phone_number':user_data.phone_number,'description':user_data.description})
    return render(request, 'edit_company_profile.html', {'form': form})


def main_page_human(request):
    email=request.session['email']
    otherdata=User.objects.filter(email=email)
    user_id=otherdata[0].id
    if User.objects.filter(email=email).exists():
        otherdata=User.objects.filter(email=email)
        usertype=otherdata[0].type
    if 'ad_search' in request.POST and request.method == 'POST':
        form = SearchBarForm(request.POST)
        if form.is_valid():
            searchBar = form.cleaned_data.get("searchBar")
            job_location = form.cleaned_data.get("job_location")
            department = form.cleaned_data.get("department")
            job_type = form.cleaned_data.get("job_type")
            study_level = form.cleaned_data.get("study_level")
            career_level = form.cleaned_data.get("career_level")
            industry = form.cleaned_data.get("industry")
            request.session['searchBar'] = searchBar      
            request.session['job_location'] = job_location   
            request.session['department'] = department   
            request.session['job_type'] = job_type    
            request.session['study_level'] = study_level     
            request.session['career_level'] = career_level     
            request.session['industry'] = industry     
            return redirect('show_filtered_ads')
    else:
        form = SearchBarForm()
    if 'user_search' in request.POST and request.method == 'POST':
        form = MiniSearchForm(request.POST)
        if form.is_valid():
            searchBar = form.cleaned_data.get("searchBar")
            request.session['searchBar'] = searchBar
            return redirect('show_filtered_users')
        else:
            form = MiniSearchForm()   
    return render(request, 'main_page_human.html',{'form':form,'usertype':usertype,'user_id':user_id})

def main_page_company(request):
    email=request.session['email']
    otherdata=Company.objects.filter(email=email)
    company_id=otherdata[0].id
    if 'ad_search' in request.POST:
        form = SearchBarForm(request.POST)
        if form.is_valid():
            searchBar = form.cleaned_data.get("searchBar")
            job_location = form.cleaned_data.get("job_location")
            department = form.cleaned_data.get("department")
            job_type = form.cleaned_data.get("job_type")
            study_level = form.cleaned_data.get("study_level")
            career_level = form.cleaned_data.get("career_level")
            industry = form.cleaned_data.get("industry")
            request.session['searchBar'] = searchBar     
            request.session['job_location'] = job_location     
            request.session['department'] = department     
            request.session['job_type'] = job_type     
            request.session['study_level'] = study_level     
            request.session['career_level'] = career_level     
            request.session['industry'] = industry     
            return redirect('show_filtered_ads')
    else:
        form = SearchBarForm()
    if 'user_search' in request.POST:
        form = MiniSearchForm(request.POST)
        if form.is_valid():
            searchBar = form.cleaned_data.get("searchBar")
            request.session['searchBar'] = searchBar
            return redirect('show_filtered_users')
        else:
            form = MiniSearchForm()        
    return render(request, 'main_page_company.html',{'form':form,'company_id':company_id})

def new_ad(request):
    email=request.session['email']
    user_data = Company.objects.filter(email=email).first()
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            if user_data.company_name=='unspecified':
                name='unspecified'
            else:
                name=user_data.company_name
            current_date=date.today()
            phone_number = form.cleaned_data.get("phone_number")
            job_title = form.cleaned_data.get("job_title")
            job_description = form.cleaned_data.get("job_description")
            job_location = form.cleaned_data.get("job_location")
            job_type = form.cleaned_data.get("job_type")
            study_level = form.cleaned_data.get("study_level")
            department = form.cleaned_data.get("department")
            career_level = form.cleaned_data.get("career_level")
            salary = form.cleaned_data.get("salary")
            ad = Ad(company_id=user_data.id, company_name=name, industry=user_data.industry, phone_number=phone_number, job_title=job_title, job_description=job_description,job_location=job_location, salary=salary,posted_date=current_date,career_level=career_level,department=department,job_type=job_type,study_level=study_level)
            ad.save()
            return redirect('main_page_company')
    else:
        form = AdForm()
    return render(request, 'new_ad.html',{'form':form})

def show_filtered_ads(request):
    email=request.session['email']
    own_id=0
    try:
        otherdata = Company.objects.filter(email=email)
        if otherdata.exists():
            own_id = otherdata[0].id
    except Company.DoesNotExist:
        own_id=0
    searchBar=request.session['searchBar']
    job_location=request.session['job_location']     
    department=request.session['department']     
    job_type=request.session['job_type']     
    study_level=request.session['study_level']     
    career_level=request.session['career_level']     
    industry=request.session['industry']     
    mydata = Ad.objects.filter(Q(company_name__icontains=searchBar) | Q(job_title__icontains=searchBar) | Q(job_description__icontains=searchBar))
    if job_location!='Unspecified':
        mydata=mydata.filter(job_location__exact=job_location)
    if department!='Unspecified':
        mydata=mydata.filter(department__exact=department)
    if job_type!='Unspecified':
        mydata=mydata.filter(job_type__exact=job_type)
    if study_level!='Unspecified':
        mydata=mydata.filter(study_level__exact=study_level)
    if career_level!='Unspecified':
        mydata=mydata.filter(career_level__exact=career_level)
    if industry!='Unspecified':
        mydata=mydata.filter(industry__exact=industry)
    context={'mymembers': mydata,
             'own_id':own_id

    }
    return render(request, 'show_filtered_ads.html', context=context)

def show_filtered_ads_not_logged(request):
    searchBar=request.session['searchBar']
    job_location=request.session['job_location']     
    department=request.session['department']     
    job_type=request.session['job_type']     
    study_level=request.session['study_level']    
    career_level=request.session['career_level']     
    industry=request.session['industry']     
    mydata = Ad.objects.filter(Q(company_name__icontains=searchBar) | Q(job_title__icontains=searchBar) | Q(job_description__icontains=searchBar))
    if job_location!='Unspecified':
        mydata=mydata.filter(job_location__exact=job_location)
    if department!='Unspecified':
        mydata=mydata.filter(department__exact=department)
    if job_type!='Unspecified':
        mydata=mydata.filter(job_type__exact=job_type)
    if study_level!='Unspecified':
        mydata=mydata.filter(study_level__exact=study_level)
    if career_level!='Unspecified':
        mydata=mydata.filter(career_level__exact=career_level)
    if industry!='Unspecified':
        mydata=mydata.filter(industry__exact=industry)
    context={'mymembers': mydata

    }
    return render(request, 'show_filtered_ads_not_logged.html', context=context)

def show_filtered_users(request):
    searchBar=request.session['searchBar']
    email=request.session['email']
    if User.objects.filter(email=email).exists():
        otherdata=User.objects.filter(email=email)
        own_id=otherdata[0].id
    elif Company.objects.filter(email=email).exists():
        otherdata=Company.objects.filter(email=email)
        own_id=otherdata[0].id
    mydata = User.objects.filter(Q(full_name__icontains=searchBar)).exclude(
    Q(full_name__icontains="admin") |
    Q(full_name__icontains="Admin") |
    Q(full_name__icontains="unspecified") 
)   
    mydata2 = Company.objects.filter(Q(company_name__icontains=searchBar))
    context={'myusers': mydata,
             'mycompanies': mydata2,
             'own_id':own_id
    }
    return render(request, 'show_filtered_users.html', context=context)

def company_profile(request,company_id):
    email=request.session['email']
    if Company.objects.filter(email=email).exists():
        otherdata=Company.objects.filter(email=email)
        usertype=otherdata[0].type
    elif User.objects.filter(email=email).exists():
        otherdata=User.objects.filter(email=email)
        usertype=otherdata[0].type 
    mydata = Company.objects.filter(id=company_id)
    context = {
        'mymembers': mydata,
        'usertype':usertype
    }
    if 'admin_delete' in request.POST:
        Company_delete(company_id)
        return redirect('main_page_human')
    return render(request, 'company_profile.html',context=context)

def human_profile(request,user_id):
    email=request.session['email']
    if User.objects.filter(email=email).exists():
        otherdata=User.objects.filter(email=email)
        usertype=otherdata[0].type
    else: 
        otherdata=Company.objects.filter(email=email)
        usertype=otherdata[0].type
    mydata = User.objects.filter(id=user_id)
    context = {
        'mymembers': mydata,
        'usertype':usertype
        
    }
    if 'admin_delete' in request.POST:
        Human_delete(user_id)
        return redirect('main_page_human')

    return render(request, 'human_profile.html',context=context)
        
def own_company_profile(request,company_id):
    email=request.session['email']
    mydata=Company.objects.filter(email=email)
    ads=Ad.objects.filter(company_id=mydata[0].id)
    context = {
        'mymembers': mydata,
        'ads':ads
    }
    return render(request, 'own_company_profile.html',context=context)

def own_human_profile(request,user_id):
    email=request.session['email']
    mydata=User.objects.filter(email=email)
    used_id=mydata[0].id
    applications = Application.objects.filter(user_id=used_id)
    applies = applications.values_list('ad_id', flat=True)
    ads = Ad.objects.filter(id__in=applies)
    context = {
        'mymembers': mydata,
        'ads': ads
    }
    return render(request, 'own_human_profile.html',context=context)

def ad_page(request,ad_id):
    mydata = Ad.objects.filter(id=ad_id)
    email=request.session['email']
    used_id=0
    user_list='None'
    already_applied='False'
    otherdata='None'
    if email=='None':
        usertype='None'
    elif User.objects.filter(email=email).exists():
        otherdata=User.objects.filter(email=email)
    elif Company.objects.filter(email=email).exists():
        otherdata=Company.objects.filter(email=email)
    if otherdata!='None':
        usertype=otherdata[0].type
        used_id=otherdata[0].id
        if Application.objects.filter(ad_id=ad_id, user_id=used_id).exists():
            already_applied=True
        else:
            already_applied=False
        application_list = Application.objects.filter(ad_id=ad_id)
        applies = application_list.values_list('user_id', flat=True)
        user_list = User.objects.filter(id__in=applies)
    if Application.objects.filter(ad_id=ad_id).exists():
        applicationlist=Application.objects.filter(ad_id=ad_id)
        users_who_applied = [application.user for application in applicationlist]
    else:
        users_who_applied=[]
    context = {
        'mymembers': mydata,
        'usertype':usertype,
        'userid':used_id,
        'applies':user_list,
        'ad_id':ad_id,
        'already_applied':already_applied,
        'applicationlist':users_who_applied,
    }
    comp_id = mydata[0].company_id
    newdata=Company.objects.filter(id=comp_id)
    email1=newdata[0].email
    if 'human_submit' in request.POST:
        subject = 'Job application sent'
        message = f'Dear {otherdata[0].full_name},\n\n Your job application has been sent.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email1, ]
        send_mail( subject, message, email_from, recipient_list )
        cursor = connection.cursor()
        cursor.execute("INSERT INTO jobsite_application (ad_id, user_id) VALUES (%s, %s)", [ ad_id, otherdata[0].id, ])
        connection.commit()
        connection.close()
        return redirect('ad_page', ad_id=ad_id)
    elif 'human_unapply' in request.POST:
        Application_delete(ad_id,otherdata[0].id)
        return redirect('ad_page', ad_id=ad_id)
    elif 'admin_delete' in request.POST:
        Ad_delete(ad_id)
        return redirect('main_page_human')
    elif 'company_delete' in request.POST:
        Ad_delete(ad_id)
        return redirect('main_page_company')
    elif 'delete_application' in request.POST:
        user_id = request.POST.get('user_id')
        Application_delete(ad_id,user_id)
        return redirect('ad_page',ad_id=ad_id)
    return render(request, 'ad_page.html',context=context)

def Application_delete(ad_id,user_id):
    del_apply=Application.objects.get(ad_id=ad_id,user_id=user_id)
    del_apply.delete()

def Ad_delete(ad_id):
    del_ad = Ad.objects.get(id=ad_id)
    del_ad.delete()

def Human_delete(user_id):
    del_user = User.objects.get(id=user_id)
    del_user.delete()

def Company_delete(user_id):
    del_company = Company.objects.get(id=user_id)
    del_company.delete()





