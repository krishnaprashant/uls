from django.db import models

# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug =  models.CharField(max_length=200)
    body = models.TextField()
    blog_picture = models.ImageField(upload_to="static\\blogs")
    mark_popular = models.BooleanField(null=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
