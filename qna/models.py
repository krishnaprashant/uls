from django.db import models
from home.models import User
# Create your models here.

class Qna(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.TextField(null=True)



class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qna = models.ForeignKey(Qna, on_delete=models.CASCADE)
    comment= models.TextField(null=True)
