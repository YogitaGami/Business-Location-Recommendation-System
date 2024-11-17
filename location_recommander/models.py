from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class LoginForm(models.Model):
    user= models.CharField(max_length = 100)
    password = models.CharField(max_length= 50)

class Contact(models.Model):
    name=models.CharField(max_length=122)
    email=models.CharField(max_length=122)
    phone=models.CharField(max_length=122)
    desc=models.TextField()
    date=models.DateField()
    def __str__(self):
        return self.name
   
class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Business_search = models.CharField(max_length=100)
    result = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} searched for {self.Business_search}'  