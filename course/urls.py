from django.urls import path, include
from . import views


urlpatterns = [    
    path('',views.home,name="course"),
    path('<str:slug>',views.get_course_details,name="get_course_details"),
    path('<str:slug>/<str:city>',views.get_course_details_city,name="get_course_details"),
]
