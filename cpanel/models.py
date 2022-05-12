from django.db import models
import random
import string
# Create your models here.



class Content(models.Model):
    content = models.TextField()

class Section(models.Model):
    content = models.ForeignKey(Content,on_delete=models.CASCADE)
    location = models.TextField()

class CustomSection(models.Model):
    url = models.TextField()
    content = models.TextField()
