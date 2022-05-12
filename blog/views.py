from django.core import paginator
from helpers.basic import pprint
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse
from django.contrib import messages
from .models import Blog as BlogData
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from home.models import User
from django.db.models import Q
from django.template.base import VariableDoesNotExist
from cpanel.models import Content,Section

# Create your views here.




class MarkedBlogs(View):

    def get(self, request):
        marked_blogs = BlogData.objects.filter(mark_popular=1)
        return render(request,'marked-blogs.html',{'blogs':marked_blogs})


def view_blog(request):
    content = str(object='')
    try:
        section = Section.objects.get(pk=1)
        content = section.content.content
    except:
        pass
    try:
        page_number = request.GET.get('page')
        blogs = BlogData.objects.all()
        count = blogs.count()
        popular = BlogData.objects.filter(mark_popular=True)
        blogs = Paginator(blogs,3)
        onset = (int(page_number) * 3 ) - 3
        offset = int(page_number) *  3
        string_slice = f"{onset}:{offset}"
        page_number = int(page_number)
        previous = int(page_number - 1)
        next = int(page_number + 1)
        return render(request,'blog-feed.html',{"blogs":blogs,"string_slice":string_slice,'popular':popular,'count':count,"page_number":page_number,'previous':previous,'next':next,'content':content})
    except TypeError:
        return redirect(f"{reverse('Feeds')}?page=1")


def search_blog(request):
    try:
        page_number = request.GET.get('page')
        if page_number == "":
            page_number = 1
        q = request.GET.get('q')
        if q == "":
            return render(request,'blog-not-found.html',{'title':'empty query'})
        blogs = BlogData.objects.filter(
            Q(title__icontains=q) | Q(slug__icontains=q) | Q(body__icontains=q)
        )
        count = blogs.count()
        if not count:
            return render(request,'blog-not-found.html',{'title':q})
        popular = BlogData.objects.filter(mark_popular=True)
        blogs = Paginator(blogs, 3)
        onset = (int(page_number) * 3 ) - 3
        offset = int(page_number) *  3
        string_slice = f"{onset}:{offset}"
        page_number = int(page_number)
        previous = int(page_number - 1)
        next = int(page_number + 1)
        return render(request,'blog-feed.html',{"blogs":blogs,"string_slice":string_slice,'popular':popular,'count':count,"page_number":page_number,'previous':previous,'next':next})
    except TypeError:
        return redirect(f"{reverse('blog.search')}?page=1")
    except VariableDoesNotExist:
        return render(request,'blog-not-found.html',{'title':q})

def blog_details(request,slug):
    id = request.GET.get('id')
    blog = BlogData.objects.get(slug=slug)
    count = BlogData.objects.all().count()
    popular = BlogData.objects.filter(mark_popular=True)
    students_enrolled = User.objects.filter(usertype='user').count()
    return render(request,'blog-details.html',{'blog':blog,'students_enrolled':students_enrolled,'popular':popular,'count':count})
