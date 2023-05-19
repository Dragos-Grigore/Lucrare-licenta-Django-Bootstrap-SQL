from django.db import models

class User(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    full_name = models.CharField(max_length=50)
    phone_number=models.CharField(max_length=20)
    education=models.CharField(max_length=500)
    experience=models.CharField(max_length=500)
    skills=models.CharField(max_length=500)
    hobbies=models.CharField(max_length=500)
    foreign_languages=models.CharField(max_length=500)

    def __str__(self):
        return ' '.join([self.full_name,self.email,self.password,self.type])

