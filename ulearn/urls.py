from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('',include("home.urls")),
    path('cpanel/',include("cpanel.urls")),
    path('blog/',include("blog.urls")),
    path('pgen/',include("pgen.urls")),
    path('course/',include("course.urls")),
    path('<str:country>/course/',include("course.urls")),
    path('training/',include("training.urls")),
    path('search/',include("search.urls")),
    path('events/',include("event.urls")),
    path('pum/',include("PUM.urls")),
    path('qna/',include("qna.urls")),
]
