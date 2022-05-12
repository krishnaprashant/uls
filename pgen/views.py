from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse,request
from django.urls import reverse
from .forms import AddDataForm, AddCourseForm
from django.contrib import messages
# Create your views here.


class AddData(View):
    
    VALIDATE_FORM = None
    MODEL_NAME = ""
    TEMPLATE_NAME = ""
    URL_NAME = ""

    def __init__(self):
        self.MODEL_NAME = ""
        self.TEMPLATE_NAME = ""
        self.RESPONSE_MESSAGE = ""
        self.URL_NAME = ""
        self.VALIDATE_FORM = None

    def get(self,request):
        fm = {}
        return render(request, F'{self.TEMPLATE_NAME}', {
            'form': fm
        })

    def post(self, request):
        ab = {}        
        ab = self.VALIDATE_FORM(request.POST,request.FILES)
        if not ab.is_valid():
            return render(request, self.TEMPLATE_NAME, {
                'form': ab
            })
        self.db_add(request)        
        messages.info(request, self.RESPONSE_MESSAGE)
        return redirect(reverse(self.URL_NAME))
    
    def db_add(self,request):
        pass
    def update_db(self,request):
        pass

class UpdateData(View):
    
    VALIDATE_FORM = None
    MODEL_NAME = ""
    TEMPLATE_NAME = ""
    URL_NAME = ""

    def __init__(self):
        self.MODEL_NAME = ""
        self.TEMPLATE_NAME = ""
        self.RESPONSE_MESSAGE = ""
        self.URL_NAME = ""
        self.VALIDATE_FORM = None

    def get(self,request):
        fm = {}
        return render(request, F'{self.TEMPLATE_NAME}', {
            'form': fm
        })

    def post(self, request):
        ab = {}        
        ab = self.VALIDATE_FORM(request.POST,request.FILES)
        if not ab.is_valid():
            return render(request, self.TEMPLATE_NAME, {
                'form': ab
            })
        self.db_add(request)        
        messages.info(request, self.RESPONSE_MESSAGE)
        return redirect(reverse(self.URL_NAME))
           
    def update_db(self,request):
        pass


# class AddCourse(AddData):

#     def __init__(self):
#         self.MODEL_NAME = "course"
#         self.TEMPLATE_NAME = "add-blog.html"
#         self.URL_NAME = "Blog"
#         self.RESPONSE_MESSAGE = "Blog was updated"
#         self.VALIDATE_FORM = AddCourseForm

#     def db_add(self,request):   
#         pass     
#         # b = BlogData()
#         # b.title = request.POST.get('title')
#         # b.slug = request.POST.get('slug')
#         # b.body = request.POST.get('body')
#         # b.blog_picture = request.FILES.get('blog_picture')
#         # mark_popular = request.POST.get('mark_popular')
#         # if mark_popular == 'on':
#         #     mark_popular = True
#         # else:
#         #     mark_popular = False
#         # b.mark_popular = mark_popular
#         # b.save()
