from django.db import models



class User(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    type = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'


    def __str__(self):
        return ' '.join([self.full_name,self.email,self.password,self.type])

