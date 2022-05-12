from django import forms
from django.db.models import fields
from django.db.models.query import QuerySet
from django.forms import widgets
from django.contrib.auth import get_user_model
from home.models import Course, WithCountry, WithCity, WithOutCountryCity, CourseTitle, CountryList, Faq

class AddBlogForm(forms.Form):
    title = forms.CharField(required=True)
    slug = forms.CharField(required=True)
    body = forms.CharField(required=True)
    blog_picture = forms.ImageField(required=True)
    mark_popular = forms.CharField(required=False)

class LoginForm(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(required=True)

class UpdateBlogForm(forms.Form):
    title = forms.CharField(required=True)
    slug = forms.CharField(required=True)
    body = forms.CharField(required=True)
    blog_picture = forms.ImageField(required=False)
    mark_popular = forms.CharField(required=False)


class AddCourseForm(forms.Form):
    category = forms.CharField(required=True)
    title = forms.CharField(required=True)
    slug = forms.CharField(required=True)
    course_picture = forms.ImageField(required=True)
    mark_popular = forms.CharField(required=False)
    h1_name = forms.CharField(required=True)
    fee = forms.CharField(required=True)
    description = forms.CharField(required=True)
    key_features = forms.CharField(required=True)
    what_you_learn = forms.CharField(required=True)
    course_syllabus = forms.CharField(required=True)
    meta_title = forms.CharField(required=True)
    meta_description = forms.CharField(required=True)
    meta_keywords = forms.CharField(required=True)

class UpdateCourseForm(forms.Form):
    category = forms.CharField(required=True)
    title = forms.CharField(required=True)
    slug = forms.CharField(required=True)
    course_picture = forms.ImageField(required=False)
    mark_popular = forms.CharField(required=False)
    h1_name = forms.CharField(required=True)
    fee = forms.CharField(required=True)
    description = forms.CharField(required=True)
    key_features = forms.CharField(required=True)
    what_you_learn = forms.CharField(required=True)
    course_syllabus = forms.CharField(required=True)
    meta_title = forms.CharField(required=True)
    meta_description = forms.CharField(required=True)
    meta_keywords = forms.CharField(required=True)


class AddEventsForm(forms.Form):
    title = forms.CharField(required=True)
    slug = forms.CharField(required=True)
    body = forms.CharField(required=True)
    select_country = forms.SelectMultiple()
    select_cities = forms.SelectMultiple()
    meta_title = forms.CharField(required=True)
    meta_description = forms.CharField(required=True)
    date_time = forms.DateTimeField(required=True)


class AddTrainingForm(forms.Form):
    selecting_category = forms.CharField(required=True)
    course_type = forms.CharField(required=True)
    course_name = forms.CharField(required=True)
    slug = forms.CharField(required=True)
    h1_name = forms.CharField(required=True)
    fee = forms.IntegerField(required=True)
    course_description = forms.CharField(required=True)
    course_key_features = forms.CharField(required=True)
    what_you_learn = forms.CharField(required=True)
    course_syllabus = forms.CharField(required=True)
    meta_title = forms.CharField(required=True)
    meta_description = forms.CharField(required=True)
    meta_keywords = forms.CharField(required=True)
    course_picture = forms.ImageField(required=True)

class UpdateTrainingForm(forms.Form):
    selecting_category = forms.CharField(required=True)
    course_type = forms.CharField(required=True)
    course_name = forms.CharField(required=True)
    slug = forms.CharField(required=True)
    h1_name = forms.CharField(required=True)
    course_description = forms.CharField(required=True)
    course_key_features = forms.CharField(required=True)
    what_you_learn = forms.CharField(required=True)
    course_syllabus = forms.CharField(required=True)
    meta_title = forms.CharField(required=True)
    meta_description = forms.CharField(required=True)
    meta_keywords = forms.CharField(required=True)
    course_picture = forms.ImageField(required=False)

class AddSectionForm(forms.Form):
    content_id = forms.CharField(required=True)
    location = forms.CharField(required=True)


class WithCountryForm(forms.ModelForm):

    class Meta:
        model = WithCountry
        fields = '__all__'
        exclude = ['course_code']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control','placeholder': 'Course'}),
            'description': forms.Textarea(attrs={'class': 'form-control summernote', 'placeholder': 'Description'}),
            'features':forms.Textarea(attrs={'class':'form-control summernote','placeholder': 'Features'}),
            'learn':forms.Textarea(attrs={'class':'form-control summernote','placeholder': 'Learn'}),
            'syllabus':forms.Textarea(attrs={'class':'form-control summernote','placeholder': 'Syllabus'}),
            'country':forms.SelectMultiple(attrs={'class':'form-control multipleSelect','placeholder': 'Country'}),
            'course_code':forms.TextInput(attrs={'class':'form-control','placeholder': 'Course Code'}),
            'scheduled_dates':forms.TextInput(attrs={'class':'form-control','placeholder': 'Scheduled Dates'}),
            'scheduled_times':forms.TextInput(attrs={'class':'form-control','placeholder': 'Scheduled Times'}),
            'course_language':forms.TextInput(attrs={'class':'form-control','placeholder': 'Course Language'}),
            'currency':forms.Select(attrs={'class':'form-control','placeholder': 'Currency'}),
            'course_amount':forms.TextInput(attrs={'class':'form-control','placeholder': 'Course amount'}),
        }

class WithCountryEditForm(forms.ModelForm):

    class Meta:
        model = WithCountry
        fields = '__all__'
        exclude = ['course_code']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control','placeholder': 'Course'}),
            'description': forms.Textarea(attrs={'class': 'form-control summernote', 'placeholder': 'Description'}),
            'features':forms.Textarea(attrs={'class':'form-control summernote','placeholder': 'Features'}),
            'learn':forms.Textarea(attrs={'class':'form-control summernote','placeholder': 'Learn'}),
            'syllabus':forms.Textarea(attrs={'class':'form-control summernote','placeholder': 'Syllabus'}),
            'country':forms.TextInput(attrs={'class':'form-control','placeholder': 'Country'}),
            'course_code':forms.TextInput(attrs={'class':'form-control','placeholder': 'Course Code'}),
            'scheduled_dates':forms.TextInput(attrs={'class':'form-control','placeholder': 'Scheduled Dates'}),
            'scheduled_times':forms.TextInput(attrs={'class':'form-control','placeholder': 'Scheduled Times'}),
            'course_language':forms.TextInput(attrs={'class':'form-control','placeholder': 'Course Language'}),
            'currency':forms.Select(attrs={'class':'form-control','placeholder': 'Currency'}),
            'course_amount':forms.TextInput(attrs={'class':'form-control','placeholder': 'Course amount'}),
        }


class WithCityForm(forms.ModelForm):

    class Meta:
        model = WithCity
        fields = '__all__'
        exclude = ['course_code']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control','placeholder': 'Course'}),
            'description': forms.Textarea(attrs={'class': 'form-control summernote', 'placeholder': 'Description'}),
            'features':forms.Textarea(attrs={'class':'form-control summernote','placeholder': 'Features'}),
            'learn':forms.Textarea(attrs={'class':'form-control summernote','placeholder': 'Learn'}),
            'syllabus':forms.Textarea(attrs={'class':'form-control summernote','placeholder': 'Syllabus'}),
            'country':forms.SelectMultiple(attrs={'class':'form-control multipleSelect','placeholder': 'Country'}),
            'city':forms.TextInput(attrs={'class':'form-control','placeholder': 'City'}),
            'course_code':forms.TextInput(attrs={'class':'form-control','placeholder': 'Course Code'}),
            'scheduled_dates':forms.TextInput(attrs={'class':'form-control','placeholder': 'Scheduled Dates'}),
            'scheduled_times':forms.TextInput(attrs={'class':'form-control','placeholder': 'Scheduled Times'}),
            'course_language':forms.TextInput(attrs={'class':'form-control','placeholder': 'Course Language'}),
            'currency':forms.Select(attrs={'class':'form-control','placeholder': 'Currency'}),
            'course_amount':forms.TextInput(attrs={'class':'form-control','placeholder': 'Course amount'}),
        }

class WithCityFormEdit(forms.ModelForm):

    class Meta:
        model = WithCity
        fields = '__all__'
        exclude = ['course_code']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control','placeholder': 'Course'}),
            'description': forms.Textarea(attrs={'class': 'form-control summernote', 'placeholder': 'Description'}),
            'features':forms.Textarea(attrs={'class':'form-control summernote','placeholder': 'Features'}),
            'learn':forms.Textarea(attrs={'class':'form-control summernote','placeholder': 'Learn'}),
            'syllabus':forms.Textarea(attrs={'class':'form-control summernote','placeholder': 'Syllabus'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'city':forms.TextInput(attrs={'class':'form-control','placeholder': 'City'}),
            'course_code':forms.TextInput(attrs={'class':'form-control','placeholder': 'Course Code'}),
            'scheduled_dates':forms.TextInput(attrs={'class':'form-control','placeholder': 'Scheduled Dates'}),
            'scheduled_times':forms.TextInput(attrs={'class':'form-control','placeholder': 'Scheduled Times'}),
            'course_language':forms.TextInput(attrs={'class':'form-control','placeholder': 'Course Language'}),
            'currency':forms.Select(attrs={'class':'form-control','placeholder': 'Currency'}),
            'course_amount':forms.TextInput(attrs={'class':'form-control','placeholder': 'Course amount'}),
        }


class WithoutCityCountryForm(forms.ModelForm):

    class Meta:
        model = WithOutCountryCity
        fields = '__all__'
        exclude = ['course_code']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Course'}),
            'description': forms.Textarea(attrs={'class': 'form-control summernote', 'placeholder': 'Description'}),
            'features': forms.Textarea(attrs={'class': 'form-control summernote', 'placeholder': 'Features'}),
            'learn': forms.Textarea(attrs={'class': 'form-control summernote', 'placeholder': 'Learn'}),
            'syllabus': forms.Textarea(attrs={'class': 'form-control summernote', 'placeholder': 'Syllabus'}),
            'course_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Code'}),
            'scheduled_dates': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Scheduled Dates'}),
            'scheduled_times': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Scheduled Times'}),
            'course_language': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Language'}),
            'currency': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Currency'}),
            'course_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course amount'}),
        }

class WithoutCityCountryFormEdit(forms.ModelForm):

    class Meta:
        model = WithOutCountryCity
        fields = '__all__'
        exclude = ['course_code']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Course'}),
            'description': forms.Textarea(attrs={'class': 'form-control summernote', 'placeholder': 'Description'}),
            'features': forms.Textarea(attrs={'class': 'form-control summernote', 'placeholder': 'Features'}),
            'learn': forms.Textarea(attrs={'class': 'form-control summernote', 'placeholder': 'Learn'}),
            'syllabus': forms.Textarea(attrs={'class': 'form-control summernote', 'placeholder': 'Syllabus'}),
            'course_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Code'}),
            'scheduled_dates': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Scheduled Dates'}),
            'scheduled_times': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Scheduled Times'}),
            'course_language': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Language'}),
            'currency': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Currency'}),
            'course_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course amount'}),
        }

class AddTitleForm(forms.ModelForm):

    class Meta:
        model = CourseTitle
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Slug'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class AddFAQ(forms.ModelForm):

    class Meta:
        model = Faq
        fields = '__all__'
        widgets = {
            'course': forms.Select(attrs={'class':'form-control','placeholder':'Course'}),
            'question': forms.TextInput(attrs={'class':'form-control','placeholder':'Question'}),
            'answer': forms.TextInput(attrs={'class':'form-control','placeholder':'Answer'})
        }
