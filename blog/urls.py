from django.urls import path, include
from blog.views import view_blog
from . import views

urlpatterns = [
    path('',view_blog,name="Feeds"),
    path('<str:slug>/details/',views.blog_details,name="blog.details"),
    path('search/',views.search_blog,name="blog.search"),
    path('marked/',views.MarkedBlogs.as_view(),name="Marked"),
]
