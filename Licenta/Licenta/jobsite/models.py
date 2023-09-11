from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    full_name = models.CharField(max_length=50,default='unspecified')
    phone_number=models.CharField(max_length=20,default='unspecified')
    education = models.TextField(max_length=500, default='unspecified')
    experience=models.TextField(max_length=500, default='unspecified')
    skills=models.TextField(max_length=500, default='unspecified')
    hobbies=models.TextField(max_length=500, default='unspecified')
    foreign_languages=models.TextField(max_length=500, default='unspecified')


    def __str__(self):
        return self.email

class Company(models.Model):
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50,default='unspecified')
    industry=models.CharField(max_length=50,default='unspecified')
    phone_number = models.CharField(max_length=20, default='unspecified')
    description=models.TextField(max_length=2000, default='unspecified')

    def __str__(self):
        return self.email
    
class Ad(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, default='unspecified')
    company_name = models.CharField(max_length=100,default='unspecified')
    industry = models.CharField(max_length=50, default='unspecified')
    department= models.CharField(max_length=50,default='unspecified')
    job_type= models.CharField(max_length=50,default='unspecified')
    study_level= models.CharField(max_length=50,default='unspecified')
    career_level= models.CharField(max_length=50,default='unspecified')
    phone_number = models.CharField(max_length=20, default='unspecified')
    job_title = models.CharField(max_length=100, default='unspecified')
    job_description = models.TextField(max_length=2000, default='unspecified')
    job_location= models.CharField(max_length=50,default='unspecified')
    salary = models.CharField(max_length=10, default='unspecified')
    posted_date = models.DateField()

    def __str__(self):
        return self.job_title
    
class Application(models.Model):
    ad=models.ForeignKey(Ad, on_delete=models.CASCADE, blank=True, default='unspecified')
    user=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default='unspecified')