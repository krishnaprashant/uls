from django import http
from django.views import View
from django.http import HttpResponse, request


def url_in(request):
    return HttpResponse("url in")
