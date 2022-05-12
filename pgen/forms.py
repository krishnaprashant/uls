from django import forms
from django.contrib.auth import get_user_model


class AddDataForm(forms.Form):
    fields = '__all__'


class UpdateDataForm(forms.Form):
    fields = '__all__'


class AddCourseForm(forms.Form):
    title = forms.CharField(required=True)
    slug = forms.CharField(required=True)
    body = forms.CharField(required=True)
    blog_picture = forms.ImageField(required=True)
    mark_popular = forms.CharField(required=False)
    
