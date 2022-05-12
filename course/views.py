from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from home.models import Course, WithCity, WithCountry, WithOutCountryCity
from django.views import View
from django.core.paginator import Paginator
from django.urls import reverse
from home.models import Training
from home.models import Course, Enrollment, TrainingEnrollment, Faq
import json
from cpanel.models import Content,Section
from helpers import basic
from itertools import chain
from home.context_processors import getCountry
from django.db.models import Q
# Create your views here.



def home(request):

    content = str(object='')
    try:
        section = Section.objects.get(pk=1)
        content = section.content.content
    except:
        pass
    courses = Course.objects.all()
    training = Training.objects.all()
    return render(request,"corporate-courses.html",{
    'courses':courses,
    'training':training,
    'content':content
    })


# class MarkedCourse(View):
#
#     def get(self, request):
#         marked_blogs = Course.objects.filter(mark_popular=1)
#         return render(request, 'marked-blogs.html', {'blogs': marked_blogs})
#
#
# def view_course(request):
#     try:
#         page_number = request.GET.get('page')
#         course = Course.objects.all()
#         course = Paginator(course, 1)
#         page_number = int(page_number)
#         prev_page_number = page_number - 1
#         page_number = f"{prev_page_number}:{page_number}"
#         return render(request, 'blog-feed.html', {"course": course, "page": page_number})
#     except TypeError:
#         return redirect(f"{reverse('Feeds')}?page=1")


def get_course_details(request,slug,**kwargs):
    try:
        if request.method == "POST":
            return redirect("%s?id=%s&quantity=%s&code=%s" % (reverse('register.enroll'), request.POST.get('course_id'), request.POST.get('quant[%s]' % request.POST.get('flc')), request.POST.get('code')))
        country_code = "in"
        id = request.GET.get('id')
        count = Enrollment.objects.filter(course_id=id,user_id=request.user.id).count()
        course = Course.objects.get(slug=slug)
        faq = Faq.objects.filter(course=course)
        if 'country' in request.session.keys() and 'country' not in kwargs:
            if request.session['country'] == "":
                without = WithOutCountryCity.objects.filter(course=course)
                return render(request,'course-with-country.html',{'course':course,"count":count,"withCountry":without})
            country_code = request.session.get('country')
            return redirect(reverse('get_course_details', kwargs={'country': country_code, 'slug': slug}))
        if 'country' not in kwargs:
            without = WithOutCountryCity.objects.filter(course=course)
            return render(request,'course-with-country.html',{'course':course,"count":count,"withCountry":without})
        if 'country' in request.session.keys() and 'city' not in request.session.keys():
            country_code = request.session.get('country')
            withCountry = WithCountry.objects.filter(~Q(country__contains=country_code)).filter(course=course)
            return render(request,'course-with-country.html',{'course':course,"count":count,"withCountry":withCountry})
        withCountry = WithCountry.objects.filter(~Q(country__contains=country_code)).filter(course=course)
        withCity = WithCity.objects.filter(course=course)
        without = WithOutCountryCity.objects.filter(course=course)
        resultSet= list(chain(withCountry,withCity,without))

        return render(request,'course-with-country.html',{'course':course,"count":count,"withCountry":resultSet,'faq':faq})
    except Course.DoesNotExist:
        return render(request,'not-found.html');


def get_course_details_city(request,slug,city,**kwargs):
    if request.method == "POST":
        return redirect("%s?id=%s&quantity=%s&code=%s" % (reverse('register.enroll'), request.POST.get('course_id'), request.POST.get('quant[%s]' % request.POST.get('flc')), request.POST.get('code')))
    course = Course.objects.get(slug=slug)
    # count = Enrollment.objects.filter(course_id=id,user_id=request.user.id).count()
    withCity = WithCity.objects.filter(~Q(city__contains=city)).filter(course=course)
    return render(request,'course-with-country.html',{'course':course,"withCountry":withCity})
