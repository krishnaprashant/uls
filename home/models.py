from random import choice
from django.db import models
from django.contrib.auth.models import AbstractUser
from helpers.basic import create_new_ref_number, create_ticket
from django.utils.text import slugify

# Create your models here.

class User(AbstractUser):
    phone = models.CharField(blank=True,max_length=15)
    profile_pic = models.ImageField(upload_to="static/profile",null=True)
    city = models.CharField(blank=False,max_length=30,default="")
    country = models.CharField(blank=False,max_length=30,default="")
    usertype = models.CharField(blank=False,max_length=200,default="user")
    def __str__(self):
        return self.username

class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    course_picture = models.ImageField(upload_to="static\\course")
    mark_popular = models.BooleanField(null=True)
    category = models.CharField(null=True,max_length=200)
    h1_name = models.CharField(null=True,max_length=200)
    description = models.TextField(null=True)
    key_features = models.TextField(null=True)
    what_you_learn = models.TextField(null=True)
    course_syllabus = models.TextField(null=True)
    meta_title = models.TextField(null=True)
    meta_description = models.TextField(null=True)
    meta_keywords = models.TextField(null=True)
    user = models.ManyToManyField(User, through="Enrollment")
    fee = models.IntegerField(null=True)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return f'/course/{self.slug}'

class Enrollment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    date_enrolled = models.DateField()
    final_grade = models.CharField(max_length=1,blank=True,null=True)
    status = models.CharField(null=True,max_length=200)
    txnid = models.CharField(null=True,max_length=200)
    amount = models.IntegerField(null=True)
    class Meta:
        unique_together = ['user','course']


class Training(models.Model):
    selecting_category = models.CharField(max_length=200)
    course_type = models.CharField(max_length=200)
    course_name = models.TextField()
    slug = models.CharField(max_length=200)
    h1_name = models.CharField(max_length=200)
    course_description = models.TextField()
    course_key_features = models.TextField()
    what_you_learn = models.TextField()
    course_syllabus = models.TextField()
    meta_title = models.TextField()
    meta_description = models.TextField()
    meta_keywords = models.TextField()
    course_picture = models.TextField()
    mark_popular = models.BooleanField(null=True)
    user = models.ManyToManyField(User,through="TrainingEnrollment")
    fee = models.IntegerField(null=True)

    def __str__(self):
        return self.course_name

class TrainingEnrollment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    training = models.ForeignKey(Training,on_delete=models.CASCADE)
    date_enrolled = models.DateField()
    status = models.CharField(null=True,max_length=200)
    txnid = models.CharField(null=True,max_length=200)
    amount = models.IntegerField(null=True)
    class Meta:
        unique_together = ['user','training']


class WithCountry(models.Model):
    countries = [
        ('inr', "India"),
        ('usd', "USD")
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    features = models.TextField(null=True)
    learn = models.TextField(null=True)
    syllabus = models.TextField(null=True)
    country = models.TextField(null=True)
    course_code = models.TextField( default=create_new_ref_number)
    scheduled_dates = models.TextField(null=True)
    scheduled_times = models.TextField(null=True)
    course_language = models.TextField(max_length=15, null=True)
    currency = models.CharField(max_length=20, choices=countries, default='inr')
    course_amount = models.IntegerField(null=True)

class WithCity(models.Model):
    countries = [
        ('inr',"India"),
        ('usd',"USD")
    ]
    description = models.TextField(null=True)
    features = models.TextField(null=True)
    learn = models.TextField(null=True)
    syllabus = models.TextField(null=True)
    country = models.TextField(max_length=30,null=True)
    city = models.TextField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_code = models.TextField( default=create_new_ref_number)
    scheduled_dates = models.TextField(null=True)
    scheduled_times = models.TextField(null=True)
    course_language = models.TextField(max_length=15,null=True)
    currency = models.CharField(max_length=20, choices=countries, default='inr')
    course_amount = models.IntegerField(null=True)


class WithOutCountryCity(models.Model):
    countries = [
        ('inr', "India"),
        ('usd', "USD")
    ]
    description = models.TextField(null=True)
    features = models.TextField(null=True)
    learn = models.TextField(null=True)
    syllabus = models.TextField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_code = models.TextField( default=create_new_ref_number)
    scheduled_dates = models.TextField(null=True)
    scheduled_times = models.TextField(null=True)
    course_language = models.TextField(max_length=15, null=True)
    currency = models.CharField(max_length=20, choices=countries, default='inr')
    course_amount = models.IntegerField(null=True)


class CourseTitle(models.Model):
    course_categories = [
        ("Project Management","Project management"),
        ("Agile & Scrum","Agile & Scrum"),
        ("IT Service Management","IT Service Management"),
        ("Quality Management","Quality Management")
    ]
    title = models.TextField(null=True)
    slug = models.TextField(null=True)
    category = models.CharField(max_length=30, choices=course_categories, default='Project Management')


class EnrollmentWithCountry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    with_country = models.ForeignKey(WithCountry, on_delete=models.CASCADE)
    date_enrolled = models.DateField()
    status = models.CharField(null=True, max_length=200)
    txnid = models.CharField(null=True, max_length=200)
    amount = models.IntegerField(null=True)

    class Meta:
        unique_together = ['user', 'with_country']


class EnrollmentWithCity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    with_city = models.ForeignKey(WithCity, on_delete=models.CASCADE)
    date_enrolled = models.DateField()
    status = models.CharField(null=True, max_length=200)
    txnid = models.CharField(null=True, max_length=200)
    amount = models.IntegerField(null=True)

    class Meta:
        unique_together = ['user', 'with_city']


class EnrollmentWithOut(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    with_out = models.ForeignKey(WithOutCountryCity, on_delete=models.CASCADE)
    date_enrolled = models.DateField()
    status = models.CharField(null=True, max_length=200)
    txnid = models.CharField(null=True, max_length=200)
    amount = models.IntegerField(null=True)

    class Meta:
        unique_together = ['user', 'with_out']

class ErrorLog(models.Model):
    error = models.TextField(null=True)
    ts = models.DateTimeField()
    ticket_number = models.TextField(default=create_ticket)

class CountryList(models.Model):
    country_code = models.CharField(null=True, max_length=50)
    country_name = models.CharField(null=True, max_length=50)
    currency = models.CharField(null=True, max_length=50)
    region = models.CharField(null=True, max_length=50)

    def get_absolute_url(self):
        return f'course/{self.country_name}'


class CityList(models.Model):
    city_name = models.CharField(null=True,max_length=50)
    country_code = models.CharField(null=True,max_length=10)

class Faq(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.TextField(null=True)
    answer = models.TextField(null=True)

class Snippet(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, null=True)
    body = models.TextField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args,**kwargs)
    def get_absolute_url(self):
        return f'/{self.slug}'
