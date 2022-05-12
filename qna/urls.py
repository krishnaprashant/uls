from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name="qna_home"),
    path('thread', views.post_thread, name="qna_thread"),
]
