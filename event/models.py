from django.db import models
from django.forms.widgets import DateTimeInput

# Create your models here.


class Events(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    body = models.TextField()
    select_country = models.CharField(max_length=200)
    select_cities = models.CharField(max_length=200)
    meta_title = models.TextField()
    meta_description = models.TextField()
    date_time = models.DateTimeField()