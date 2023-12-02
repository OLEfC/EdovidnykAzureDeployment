
# Create your models here.
# models.py
from django.db import models

class CustomUser(models.Model):
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()
    birthdate = models.DateField()

