from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home,name="training_home"),    
    path('details',views.details,name="training.details"),    
]
