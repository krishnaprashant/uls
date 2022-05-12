from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from home.models import Course
from helpers.basic import pprint
from django.core import serializers
from django.db.models import Q
# Create your views here.


def search(request):
    q = request.GET.get('q')
    c = Course.objects.filter(
        Q(title__icontains=q) | Q(slug__icontains=q) 
    )
    # data = serializers.serialize('json', c)
    # return HttpResponse(data, content_type='application/json')
    return render(request,"results.html",{"course":c})
