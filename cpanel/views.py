from django import http
import django
from django.db.models import fields
from event.models import Events
from home.models import CourseTitle, Training, WithCity, WithCountry, WithOutCountryCity, CountryList, CityList, Faq
import json
from django import views
from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse, request
from django.views import View
from django.urls import reverse
from django.contrib import messages
from blog.models import Blog as BlogData
from django.core.paginator import Paginator
from django.core import paginator
from .forms import AddBlogForm, AddEventsForm, UpdateBlogForm, AddCourseForm, AddTrainingForm, UpdateTrainingForm, LoginForm, AddSectionForm, UpdateCourseForm, WithoutCityCountryForm, WithCountryEditForm, WithCityFormEdit, WithoutCityCountryFormEdit, AddFAQ
from django.views import View
from helpers.basic import pprint
from home.models import Course
from helpers.basic import pprint
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import auth
from django.utils.html import escape
from django.core.exceptions import PermissionDenied
from home.models import Enrollment
from django.forms.models import model_to_dict
from .models import Content, Section, CustomSection
import base64
from .forms import WithCountryForm, WithCityForm, AddTitleForm




# Create your views here.

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrap(request,*args,**kwargs):
            if not request.user.is_authenticated:
                messages.info(request,"Permission denied")
                return redirect(reverse('login'))
            if request.user.usertype in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                messages.info(request,"Permission denied")
                return redirect(reverse('login'))
        return wrap
    return decorator



def cpanel_login(request):
    fm = {}
    if request.method == "POST":
        fm = LoginForm(request.POST)
        if fm.is_valid():
            user_email = fm.cleaned_data['email']
            user_password = fm.cleaned_data['password']
            user = auth.authenticate(username=user_email, password=user_password)
            if user is not None:
                auth.login(request, user)
                # request.session['tenant_url'] = request.user.userprofile.tenant_id
                # request.session['api_token'] = request.user.userprofile.api_token
                if request.GET.get('next') is not None:
                    return redirect(request.GET.get('next'))
                return redirect(reverse("AdminHome"))
            else:
                messages.error(request, "Wrong Credentials", True)
        else:
            pass
    else:
        pass
    return render(request, "accounts/login.html", {
        'form': fm
    })


@role_required(allowed_roles=["admin"])
def home(request):
    total = Course.objects.all()
    return render(request,'cpanel_view/index.html',{
    'total': total
    })


@role_required(allowed_roles=["admin"])
def get_enrolled(request):
    e = Enrollment.objects.all()
    return render(request,'cpanel_view/list-enrolled.html',{
    'enrolled':e
    })


@role_required(allowed_roles=["admin"])
def save_to(request,path,file):
    pic = request.FILES.get(file)
    fs = FileSystemStorage()
    filename = fs.save(f"static//{path}//{pic.name}", pic)
    uploaded_file_url = fs.url(filename)
    return uploaded_file_url


class Blog(View):

    @method_decorator(role_required(allowed_roles=["admin"]))
    def get(self, request):
        fm = {}
        return render(request, 'cpanel_view/add-blog.html', {
            'form': fm
        })
    @method_decorator(role_required(allowed_roles=["admin"]))
    def post(self, request):
        ab = {}
        ab = AddBlogForm(request.POST, request.FILES)
        if not ab.is_valid():
            return render(request, 'cpanel_view/add-blog.html', {
                'form': ab
            })
        b = BlogData()
        b.title = request.POST.get('title')
        b.slug = request.POST.get('slug')
        b.body = request.POST.get('body')
        b.blog_picture = save_to(request,"blogs","blog_picture")
        mark_popular = request.POST.get('mark_popular')
        if mark_popular == 'on':
            mark_popular = True
        else:
            mark_popular = False
        b.mark_popular = mark_popular
        b.save()
        messages.info(request, "Blog was successfully added")
        return redirect(reverse('Blog'))


class ListBlog(View):
    @method_decorator(role_required(allowed_roles=["admin"]))
    def get(self,request):
        blogs = BlogData.objects.all()
        return render(request, 'cpanel_view/list-blog.html', {"blogs": blogs})


class UpdateBlog(View):
    @method_decorator(role_required(allowed_roles=["admin"]))
    def get(self,request):
        fm = {}
        blogs = BlogData.objects.get(id=request.GET.get('id'))
        return render(request, 'cpanel_view/update-blog.html', {
            'form': fm,
            'blogs':blogs
        })
    @method_decorator(role_required(allowed_roles=["admin"]))
    def post(self, request):
        ab = {}
        ab = UpdateBlogForm(request.POST, request.FILES)
        if not ab.is_valid():
            return render(request, 'cpanel_view/add-blog.html', {
                'form': ab
        })
        mark_popular = request.POST.get('mark_popular')
        if mark_popular == 'on':
            mark_popular = True
        else:
            mark_popular = False
        if len(request.FILES) > 0:
            b = BlogData.objects.filter(id=request.POST.get('blog_id')).update(
                title=request.POST.get('title'),
                slug=request.POST.get('slug'),
                body=request.POST.get('body'),
                blog_picture = save_to(request,"blogs","blog_picture"),
                mark_popular = mark_popular
            )
        else:
            b = BlogData.objects.filter(id=request.POST.get('blog_id')).update(
                title=request.POST.get('title'),
                slug=request.POST.get('slug'),
                body=request.POST.get('body'),
                mark_popular=mark_popular
            )
        messages.info(request, "Blog was successfully Updated")
        return redirect(f"{reverse('UpdateBlogForm')}?id={request.POST.get('blog_id')}")


class AddCourse(View):
    @method_decorator(role_required(allowed_roles=["admin"]))
    def get(self, request):
        courseTitle = CourseTitle.objects.all()
        fm = {}
        return render(request, 'cpanel_view/add-course.html', {
            'form': fm,
            'courseTitle': courseTitle
        })
    @method_decorator(role_required(allowed_roles=["admin"]))
    def post(self,request):
        ac = {}
        ac = AddCourseForm(request.POST, request.FILES)
        if not ac.is_valid():
            return render(request, 'cpanel_view/add-course.html', {
                'form': ac
            })
        c = Course()
        c.category = request.POST.get('category')
        c.title = request.POST.get('title')
        c.h1_name = request.POST.get('h1_name')
        c.fee = request.POST.get('fee')
        c.description = request.POST.get('description')
        c.key_features = request.POST.get('key_features')
        c.what_you_learn = request.POST.get('what_you_learn')
        c.course_syllabus = request.POST.get('course_syllabus')
        c.meta_title = request.POST.get('meta_title')
        c.meta_description = request.POST.get('meta_description')
        c.meta_keywords = request.POST.get('meta_keywords')
        c.mark_popular = request.POST.get('mark_popular')
        c.slug = request.POST.get('slug')
        c.course_picture = save_to(request,"course","course_picture")
        mark_popular = request.POST.get('mark_popular')
        if mark_popular == 'on':
            mark_popular = True
        else:
            mark_popular = False
        c.mark_popular = mark_popular
        c.save()
        messages.info(request, "Course was successfully added")
        return redirect(reverse('AddCourse'))


class ListCourse(View):
    @method_decorator(role_required(allowed_roles=["admin"]))
    def get(self,request):
        courses = Course.objects.all()
        withCountry = WithCountry.objects.all()
        withCity = WithCity.objects.all()
        withOut = WithOutCountryCity.objects.all()
        return render(request, 'cpanel_view/list-course.html', {"courses": courses,"withCountry":withCountry,"withCity":withCity,"withOut":withOut})


class UpdateCourse(View):
    @method_decorator(role_required(allowed_roles=["admin"]))
    def get(self, request):
        fm = {}
        course = Course.objects.get(id=request.GET.get('id'))
        return render(request, 'cpanel_view/update-course.html', {
            'form': fm,
            'course': course
        })
    @method_decorator(role_required(allowed_roles=["admin"]))
    def post(self, request):
        ab = {}
        ab = UpdateCourseForm(request.POST, request.FILES)
        if not ab.is_valid():
            return render(request, 'cpanel_view/update-course.html', {
                'form': ab
            })
        mark_popular = request.POST.get('mark_popular')
        if mark_popular == 'on':
            mark_popular = True
        else:
            mark_popular = False
        if len(request.FILES) > 0:
            b = Course.objects.filter(id=request.POST.get('course_id')).update(
                title=request.POST.get('title'),
                slug=request.POST.get('slug'),
                course_picture=save_to(request,"course","course_picture"),
                mark_popular=mark_popular,
                category=request.POST.get('category'),
                h1_name=request.POST.get('h1_name'),
                fee=request.POST.get('fee'),
                description=request.POST.get('description'),
                key_features=request.POST.get('key_features'),
                what_you_learn=request.POST.get('what_you_learn'),
                course_syllabus=request.POST.get('course_syllabus'),
                meta_title=request.POST.get('meta_title'),
                meta_description=request.POST.get('meta_description'),
                meta_keywords=request.POST.get('meta_keywords')
            )
        else:
            b = Course.objects.filter(id=request.POST.get('course_id')).update(
                title=request.POST.get('title'),
                slug=request.POST.get('slug'),
                mark_popular=mark_popular,
                category = request.POST.get('category'),
                h1_name = request.POST.get('h1_name'),
                fee = request.POST.get('fee'),
                description = request.POST.get('description'),
                key_features = request.POST.get('key_features'),
                what_you_learn = request.POST.get('what_you_learn'),
                course_syllabus = request.POST.get('course_syllabus'),
                meta_title = request.POST.get('meta_title'),
                meta_description = request.POST.get('meta_description'),
                meta_keywords = request.POST.get('meta_keywords')
            )
        messages.info(request, "Course was successfully Updated")
        return redirect(f"{reverse('UpdateCourseForm')}?id={request.POST.get('course_id')}")


class AddEvent(View):
    @method_decorator(role_required(allowed_roles=["admin"]))
    def get(self, request):
        fm = {}
        return render(request, 'cpanel_view/add-events.html', {
            'form': fm
        })
    @method_decorator(role_required(allowed_roles=["admin"]))
    def post(self, request):
        ae = {}
        ae = AddEventsForm(request.POST, request.FILES)
        if not ae.is_valid():
            return render(request, 'cpanel_view/add-events.html', {
                'form': ae
            })
        e = Events()
        e.title = request.POST.get('title')
        e.slug = request.POST.get('slug')
        e.body = request.POST.get('body')
        e.select_country = ",".join(request.POST.getlist('select_country'))
        e.select_cities = ",".join(request.POST.getlist('select_cities'))
        e.meta_title = request.POST.get('meta_title')
        e.meta_description = request.POST.get('meta_description')
        e.date_time = request.POST.get('date_time')
        e.save()
        messages.info(request, "Event was successfully added")
        return redirect(reverse('AddEvent'))


class UpdateEvent(View):
    @method_decorator(role_required(allowed_roles=["admin"]))
    def get(self, request):
        fm = {}
        Event = Events.objects.get(id=request.GET.get('id'))
        return render(request, 'cpanel_view/update-events.html', {
            'form': fm,
            'event': Event
        })
    @method_decorator(role_required(allowed_roles=["admin"]))
    def post(self, request):
        ae = {}
        Event = Events.objects.get(id=request.POST.get('event_id'))
        ae = AddEventsForm(request.POST, request.FILES)
        if not ae.is_valid():
            return render(request, 'cpanel_view/update-events.html', {
                'form': ae,
                'event': Event
            })
        Events.objects.filter(id=request.POST.get('event_id')).update(
            title = request.POST.get('title'),
            slug = request.POST.get('slug'),
            body = request.POST.get('body'),
            select_country = ",".join(request.POST.getlist('select_country')),
            select_cities = ",".join(request.POST.getlist('select_cities')),
            meta_title = request.POST.get('meta_title'),
            meta_description = request.POST.get('meta_description'),
            date_time = request.POST.get('date_time')
        )
        messages.info(request, "Event was successfully udated")
        return redirect(f"{reverse('UpdateEventForm')}?id={request.POST.get('event_id')}")


class ListEvents(View):
    @method_decorator(role_required(allowed_roles=["admin"]))
    def get(self,request):
        events = Events.objects.all()
        return render(request, 'cpanel_view/list-events.html', {"events": events})

class AddTraining(View):
    @method_decorator(role_required(allowed_roles=["admin"]))
    def get(self, request):
        fm = {}
        return render(request, 'cpanel_view/add-trainings.html', {
            'form': fm
        })
    @method_decorator(role_required(allowed_roles=["admin"]))
    def post(self, request):
        ae = {}
        ae = AddTrainingForm(request.POST, request.FILES)
        if not ae.is_valid():
            return render(request, 'cpanel_view/add-trainings.html', {
                'form': ae
            })
        t = Training()
        t.selecting_category = request.POST.get('selecting_category')
        t.course_type = request.POST.get('course_type')
        t.course_name = request.POST.get('course_name')
        t.slug = request.POST.get('slug')
        t.h1_name = request.POST.get('h1_name')
        t.fee = request.POST.get('fee')
        t.course_description = request.POST.get('course_description')
        t.course_key_features = request.POST.get('course_key_features')
        t.what_you_learn = request.POST.get('what_you_learn')
        t.course_syllabus = request.POST.get('course_syllabus')
        t.meta_title = request.POST.get('meta_title')
        t.meta_description = request.POST.get('meta_description')
        t.meta_keywords = request.POST.get('meta_keywords')
        t.course_picture = save_to(request,"training","course_picture")
        mark_popular = request.POST.get('mark_popular')
        if mark_popular == 'on':
            mark_popular = True
        else:
            mark_popular = False
        t.mark_popular = mark_popular
        t.save()
        messages.info(request, "Training was successfully added")
        return redirect(reverse('AddTraining'))


class UpdateTraining(View):
    @method_decorator(role_required(allowed_roles=["admin"]))
    def get(self, request):
        fm = {}
        trainings = Training.objects.get(id=request.GET.get('id'))
        return render(request, 'cpanel_view/update-trainings.html', {
            'form': fm,
            'trainings': trainings
        })
    @method_decorator(role_required(allowed_roles=["admin"]))
    def post(self, request):
        ae = {}
        trainings = Training.objects.get(id=request.POST.get('training_id'))
        ae = UpdateTrainingForm(request.POST, request.FILES)
        if not ae.is_valid():
            return render(request, 'cpanel_view/update-trainings.html', {
                'form': ae,
                'trainings': trainings
            })
        mark_popular = request.POST.get('mark_popular')
        if mark_popular == 'on':
            mark_popular = True
        else:
            mark_popular = False


        if len(request.FILES) > 0:
            Training.objects.filter(id=request.POST.get('training_id')).update(
                selecting_category = request.POST.get('selecting_category'),
                course_type = request.POST.get('course_type'),
                course_name = request.POST.get('course_name'),
                slug = ",".join(request.POST.getlist('slug')),
                h1_name = ",".join(request.POST.getlist('h1_name')),
                fee = ",".join(request.POST.getlist('fee')),
                course_description = request.POST.get('course_description'),
                course_key_features = request.POST.get('course_key_features'),
                what_you_learn = request.POST.get('what_you_learn'),
                course_syllabus = request.POST.get('course_syllabus'),
                meta_title = request.POST.get('meta_title'),
                meta_description = request.POST.get('meta_description'),
                meta_keywords = request.POST.get('meta_keywords'),
                course_picture = save_to(request,"training","course_picture"),
                mark_popular = mark_popular
            )
        else:
            Training.objects.filter(id=request.POST.get('training_id')).update(
                selecting_category = request.POST.get('selecting_category'),
                course_type = request.POST.get('course_type'),
                course_name = request.POST.get('course_name'),
                slug = ",".join(request.POST.getlist('slug')),
                h1_name = ",".join(request.POST.getlist('h1_name')),
                fee = ",".join(request.POST.getlist('fee')),
                course_description = request.POST.get('course_description'),
                course_key_features = request.POST.get('course_key_features'),
                what_you_learn = request.POST.get('what_you_learn'),
                course_syllabus = request.POST.get('course_syllabus'),
                meta_title = request.POST.get('meta_title'),
                meta_description = request.POST.get('meta_description'),
                meta_keywords = request.POST.get('meta_keywords'),
                mark_popular = mark_popular
            )
        messages.info(request, "Training was successfully udated")
        return redirect(f"{reverse('UpdateTrainingForm')}?id={request.POST.get('training_id')}")


class ListTrainings(View):
    @method_decorator(role_required(allowed_roles=["admin"]))
    def get(self,request):
        trainings = Training.objects.all()
        return render(request, 'cpanel_view/list-trainings.html', {"trainings": trainings})






@role_required(allowed_roles=["admin"])
def delete_blog(request):
    id = request.GET.get('id')
    b = BlogData.objects.filter(id=id)
    b.delete()
    messages.info(request,"Blog was deleted.")
    return redirect(reverse('ListBlog'))


@role_required(allowed_roles=["admin"])
def delete_course(request):
    id = request.GET.get('id')
    c = Course.objects.filter(id=id)
    c.delete()
    messages.info(request, "Course was deleted.")
    return redirect(reverse('ListCourse'))


@role_required(allowed_roles=["admin"])
def delete_event(request):
    id = request.GET.get('id')
    e = Events.objects.filter(id=id)
    e.delete()
    messages.info(request, "Event was deleted.")
    return redirect(reverse('ListEvents'))


@role_required(allowed_roles=["admin"])
def delete_training(request):
    id = request.GET.get('id')
    t = Training.objects.filter(id=id)
    t.delete()
    messages.info(request, "Training was deleted.")
    return redirect(reverse('ListTrainings'))



@role_required(allowed_roles=["admin"])
def AddSection(request):
    fm = {}
    if request.method == "POST":
        fm = AddSectionForm(request.POST)
        if fm.is_valid():
            Section.objects.create(content_id=request.POST.get('content_id'),location=request.POST.get('location'))
            messages.success(request, "Your Section is added.")
            return redirect(reverse('cpanel.AddSection'))
            return HttpResponse("correct")
    content = Content.objects.values('id')
    return render(request,'cpanel_view/add-section.html',{'form': fm,'content':content})


@role_required(allowed_roles=["admin"])
def EditSection(request):
    section = Section.objects.all()
    return render(request,'cpanel_view/edit-section.html',{'section':section})


@role_required(allowed_roles=["admin"])
def UpdateSection(request):
    section = ""
    id = request.GET.get('id')
    section = Section.objects.get(pk=id)
    if request.method == "POST":
        section.content_id = request.POST.get('content_id')
        section.location = request.POST.get('location')
        section.save()
        messages.success(request, "Your Section is updated.")
        return redirect("%s?id=%s"%(reverse('cpanel.UpdateSection'),id))
    return render(request,'cpanel_view/update-section.html',{'section':section})

@role_required(allowed_roles=["admin"])
def DeleteSection(request):
    return HttpResponse("welcome")



@role_required(allowed_roles=["admin"])
def AddContent(request):
    if request.method == "POST":
        if request.POST.get('content') == "":
            messages.error(request, "Please enter something.")
            return redirect(reverse('cpanel.AddContent'))
        Content.objects.create(content=base64.b64encode(bytes(request.POST.get('content'), 'utf-8')))
        messages.success(request, "Your content is added.")
        return redirect(reverse('cpanel.AddContent'))
    return render(request,'cpanel_view/add-content.html')


@role_required(allowed_roles=["admin"])
def EditContent(request):
    content = Content.objects.all()
    return render(request,'cpanel_view/edit-content.html',{'content':content})


@role_required(allowed_roles=["admin"])
def UpdateContent(request):
    content_id = request.GET.get('id')
    if request.method == "POST":
        content = Content.objects.get(pk=content_id)
        content.content = base64.b64encode(bytes(request.POST.get('content'), 'utf-8'))
        content.save()
        messages.success(request,'Content is updated')
        return redirect("%s?id=%s"%(reverse('cpanel.UpdateContent'),content_id))
    content = Content.objects.get(pk=request.GET.get('id'))
    return render(request,'cpanel_view/update-content.html',{'content':content})


@role_required(allowed_roles=["admin"])
def DeleteContent(request):
    content = Content.objects.get(pk=request.GET.get('id'))
    content.delete()
    messages.success(request, "Content was deleted.")
    return redirect(reverse('cpanel.EditContent'))


@role_required(allowed_roles=["admin"])
def AddCustomContent(request):
    if request.method == "POST":
        if request.POST.get('content') == "" or request.POST.get('url') == "":
            messages.error(request,'Content is empty or url is invalid')
            return redirect(reverse('cpanel.AddCustomContent'))
        CustomSection.objects.create(url=request.POST.get('url'),content=request.POST.get('content'))
        messages.success(request,'Custom Content is Added')
        return redirect(reverse('cpanel.AddCustomContent'))
    return render(request,'cpanel_view/add-custom-content.html')

@role_required(allowed_roles=["admin"])
def EditCustomContent(request):
    customSection = CustomSection.objects.all()
    return render(request,'cpanel_view/edit-custom-content.html',{'content':customSection})

@role_required(allowed_roles=["admin"])
def UpdateCustomContent(request):
    content_id = request.GET.get('id')
    if request.method == "POST":
        content = CustomSection.objects.get(pk=content_id)
        content.content = request.POST.get('content')
        content.save()
        messages.success(request,'Content is updated')
        return redirect("%s?id=%s"%(reverse('cpanel.UpdateCustomContent'),content_id))
    content = CustomSection.objects.get(pk=request.GET.get('id'))
    return render(request,'cpanel_view/update-custom-content.html',{'content':content})


@role_required(allowed_roles=["admin"])
def DeleteCustomContent(request):
    content = CustomSection.objects.get(pk=request.GET.get('id'))
    content.delete()
    messages.error(request, "Content was deleted.")
    return redirect(reverse('cpanel.EditCustomContent'))



@role_required(allowed_roles=["admin"])
def AddCourseWith(request):
    if request.GET.get('with') == "country":
        return AddCourseWithCountry(request)
    elif request.GET.get('with') == "city":
        return AddCourseWithCity(request)
    else:
        return AddCourseWithout(request)




def AddCourseWithout(request):
    course = Course.objects.get(pk=request.GET.get('id'))

    fm = WithoutCityCountryForm()

    fm.fields['course'].initial = course
    fm.fields['description'].initial = course.description
    fm.fields['features'].initial = course.key_features
    fm.fields['learn'].initial = course.what_you_learn
    fm.fields['syllabus'].initial = course.course_syllabus
    fm.fields['course_amount'].initial = course.fee

    if request.method == 'POST':
        fm = WithoutCityCountryForm(request.POST)
        if fm.is_valid():
            wc = WithOutCountryCity()
            wc.course = fm.cleaned_data['course']
            wc.description = fm.cleaned_data['description']
            wc.features = fm.cleaned_data['features']
            wc.learn = fm.cleaned_data['learn']
            wc.syllabus = fm.cleaned_data['syllabus']
            wc.scheduled_dates = fm.cleaned_data['scheduled_dates']
            wc.scheduled_times = fm.cleaned_data['scheduled_times']
            wc.course_language = fm.cleaned_data['course_language']
            wc.currency = fm.cleaned_data['currency']
            wc.course_amount = fm.cleaned_data['course_amount']
            wc.save()
            messages.success(request, "Course has posted")
            return redirect("%s?with=&id=%s" % (reverse('cpanel.AddCourseWith'), request.GET.get('id')))

    return render(request, "cpanel_view/with/add-course.html", {'course': course, 'form': fm})

def AddCourseWithCity(request):
    course = Course.objects.get(pk=request.GET.get('id'))

    fm = WithCityForm()

    fm.fields['course'].initial = course
    fm.fields['description'].initial = course.description
    fm.fields['features'].initial = course.key_features
    fm.fields['learn'].initial = course.what_you_learn
    fm.fields['syllabus'].initial = course.course_syllabus
    fm.fields['course_amount'].initial = course.fee
    if request.method == 'POST':
        fm = WithCityForm(request.POST)
        if fm.is_valid():
            wc = WithCity()
            wc.course = fm.cleaned_data['course']
            wc.description = fm.cleaned_data['description']
            wc.features = fm.cleaned_data['features']
            wc.learn = fm.cleaned_data['learn']
            wc.syllabus = fm.cleaned_data['syllabus']
            wc.country = fm.cleaned_data['country']
            wc.city = fm.cleaned_data['city']
            wc.scheduled_dates = fm.cleaned_data['scheduled_dates']
            wc.scheduled_times = fm.cleaned_data['scheduled_times']
            wc.course_language = fm.cleaned_data['course_language']
            wc.currency = fm.cleaned_data['currency']
            wc.course_amount = fm.cleaned_data['course_amount']
            wc.save()
            messages.success(request, "Course has posted")
            return redirect("%s?with=city&id=%s" % (reverse('cpanel.AddCourseWith'), request.GET.get('id')))

    return render(request, "cpanel_view/with/add-course.html", {'course': course, 'form': fm})

def AddCourseWithCountry(request):
    course = Course.objects.get(pk=request.GET.get('id'))

    fm = WithCountryForm()

    fm.fields['course'].initial = course
    fm.fields['description'].initial = course.description
    fm.fields['features'].initial = course.key_features
    fm.fields['learn'].initial = course.what_you_learn
    fm.fields['syllabus'].initial = course.course_syllabus
    fm.fields['course_amount'].initial = course.fee

    if request.method == 'POST':
        fm = WithCountryForm(request.POST)
        if fm.is_valid():
            wc = WithCountry()
            wc.course = fm.cleaned_data['course']
            wc.description = fm.cleaned_data['description']
            wc.features = fm.cleaned_data['features']
            wc.learn = fm.cleaned_data['learn']
            wc.syllabus = fm.cleaned_data['syllabus']
            wc.country = ", ".join(request.POST.getlist('country'))
            wc.scheduled_dates = fm.cleaned_data['scheduled_dates']
            wc.scheduled_times = fm.cleaned_data['scheduled_times']
            wc.course_language = fm.cleaned_data['course_language']
            wc.currency = fm.cleaned_data['currency']
            wc.course_amount = fm.cleaned_data['course_amount']
            wc.save()
            messages.success(request, "Course has posted")
            return redirect("%s?with=country&id=%s" % (reverse('cpanel.AddCourseWith'), request.GET.get('id')))

    return render(request, "cpanel_view/with/add-course.html", {'course': course, 'form': fm})


def DeleteCourseWith(request):
    if request.GET.get('with') == "country":
        return DeleteCourseWithCountry(request)
    elif request.GET.get('with') == "city":
        return DeleteCourseWithCity(request)
    else:
        return DeleteCourseWithoutCountryCity(request)

def DeleteCourseWithCountry(request):
    withCountry = WithCountry.objects.get(pk=request.GET.get('id'))
    withCountry.delete()
    messages.error(request, "Course has been deleted")
    return redirect(reverse('ListCourse'))
def DeleteCourseWithCity(request):
    withCity = WithCity.objects.get(pk=request.GET.get('id'))
    withCity.delete()
    messages.error(request, "Course has been deleted")
    return redirect(reverse('ListCourse'))
def DeleteCourseWithoutCountryCity(request):
    without = WithOutCountryCity.objects.get(pk=request.GET.get('id'))
    without.delete()
    messages.error(request, "Course has been deleted")
    return redirect(reverse('ListCourse'))

@role_required(allowed_roles=["admin"])
def AddTitle(request):
    fm = AddTitleForm()
    if request.method == "POST":
        fm = AddTitleForm(request.POST)
        if fm.is_valid():
            courseTitle = CourseTitle()
            courseTitle.title = fm.cleaned_data['title']
            courseTitle.slug = fm.cleaned_data['slug']
            courseTitle.category = fm.cleaned_data['category']
            courseTitle.save()
            messages.success(request, "Title has posted")
            return redirect(reverse('cpanel.AddTitle'))
    courseTitle = CourseTitle.objects.all()
    return render(request, "cpanel_view/add-title.html", {'courseTitle': courseTitle, 'form': fm})


@role_required(allowed_roles=["admin"])
def DeleteTitle(request):
    courseTitle = CourseTitle.objects.get(pk=request.GET.get('id'))
    courseTitle.delete()
    messages.error(request, "Title has been deleted")
    return redirect(reverse('cpanel.AddTitle'))



@role_required(allowed_roles=["admin"])
def EditCourseWith(request):
    if request.GET.get('with') == "country":
        return EditCourseWithCountry(request)
    elif request.GET.get('with') == "city":
        return EditCourseWithCity(request)
    else:
        return EditCourseWithOut(request)


def EditCourseWithCountry(request):
    course = WithCountry.objects.get(pk=request.GET.get('id'))

    fm = WithCountryEditForm()

    fm.fields['course'].initial = course.course
    fm.fields['description'].initial = course.description
    fm.fields['features'].initial = course.features
    fm.fields['learn'].initial = course.learn
    fm.fields['syllabus'].initial = course.syllabus
    fm.fields['scheduled_dates'].initial = course.scheduled_dates
    fm.fields['scheduled_times'].initial = course.scheduled_times
    fm.fields['country'].initial = course.country
    fm.fields['course_language'].initial = course.course_language
    fm.fields['currency'].initial = course.currency
    fm.fields['course_amount'].initial = course.course_amount

    if request.method == 'POST':
        fm = WithCountryEditForm(request.POST)
        if fm.is_valid():
            wc = WithCountry.objects.get(pk=request.GET.get('id'))
            wc.course = fm.cleaned_data['course']
            wc.description = fm.cleaned_data['description']
            wc.features = fm.cleaned_data['features']
            wc.learn = fm.cleaned_data['learn']
            wc.syllabus = fm.cleaned_data['syllabus']
            wc.country = fm.cleaned_data['country']
            wc.scheduled_dates = fm.cleaned_data['scheduled_dates']
            wc.scheduled_times = fm.cleaned_data['scheduled_times']
            wc.course_language = fm.cleaned_data['course_language']
            wc.currency = fm.cleaned_data['currency']
            wc.course_amount = fm.cleaned_data['course_amount']
            wc.save()
            messages.success(request, "Course has been updated")
            return redirect("%s?with=country&id=%s" % (reverse('cpanel.EditCourseWith'), request.GET.get('id')))
    return render(request, "cpanel_view/with/edit-with.html", {'course': course, 'form': fm})

def EditCourseWithCity(request):
    course = WithCity.objects.get(pk=request.GET.get('id'))

    fm = WithCityFormEdit()

    fm.fields['course'].initial = course.course
    fm.fields['description'].initial = course.description
    fm.fields['features'].initial = course.features
    fm.fields['learn'].initial = course.learn
    fm.fields['syllabus'].initial = course.syllabus
    fm.fields['scheduled_dates'].initial = course.scheduled_dates
    fm.fields['scheduled_times'].initial = course.scheduled_times
    fm.fields['city'].initial = course.city
    fm.fields['country'].initial = course.country
    fm.fields['course_language'].initial = course.course_language
    fm.fields['currency'].initial = course.currency
    fm.fields['course_amount'].initial = course.course_amount

    if request.method == 'POST':
        fm = WithCityFormEdit(request.POST)
        if fm.is_valid():
            wc = WithCity.objects.get(pk=request.GET.get('id'))
            wc.course = fm.cleaned_data['course']
            wc.description = fm.cleaned_data['description']
            wc.features = fm.cleaned_data['features']
            wc.learn = fm.cleaned_data['learn']
            wc.syllabus = fm.cleaned_data['syllabus']
            wc.city = fm.cleaned_data['city']
            wc.country = fm.cleaned_data['country']
            wc.scheduled_dates = fm.cleaned_data['scheduled_dates']
            wc.scheduled_times = fm.cleaned_data['scheduled_times']
            wc.course_language = fm.cleaned_data['course_language']
            wc.currency = fm.cleaned_data['currency']
            wc.course_amount = fm.cleaned_data['course_amount']
            wc.save()
            messages.success(request, "Course has been updated")
            return redirect("%s?with=city&id=%s" % (reverse('cpanel.EditCourseWith'), request.GET.get('id')))
    return render(request, "cpanel_view/with/edit-with.html", {'course': course, 'form': fm})

def EditCourseWithOut(request):
    course = WithOutCountryCity.objects.get(pk=request.GET.get('id'))

    fm = WithoutCityCountryForm()

    fm.fields['course'].initial = course.course
    fm.fields['description'].initial = course.description
    fm.fields['features'].initial = course.features
    fm.fields['learn'].initial = course.learn
    fm.fields['syllabus'].initial = course.syllabus
    fm.fields['scheduled_dates'].initial = course.scheduled_dates
    fm.fields['scheduled_times'].initial = course.scheduled_times
    fm.fields['course_language'].initial = course.course_language
    fm.fields['currency'].initial = course.currency
    fm.fields['course_amount'].initial = course.course_amount

    if request.method == 'POST':
        fm = WithoutCityCountryForm(request.POST)
        if fm.is_valid():
            wc = WithOutCountryCity.objects.get(pk=request.GET.get('id'))
            wc.course = fm.cleaned_data['course']
            wc.description = fm.cleaned_data['description']
            wc.features = fm.cleaned_data['features']
            wc.learn = fm.cleaned_data['learn']
            wc.syllabus = fm.cleaned_data['syllabus']
            wc.scheduled_dates = fm.cleaned_data['scheduled_dates']
            wc.scheduled_times = fm.cleaned_data['scheduled_times']
            wc.course_language = fm.cleaned_data['course_language']
            wc.currency = fm.cleaned_data['currency']
            wc.course_amount = fm.cleaned_data['course_amount']
            wc.save()
            messages.success(request, "Course has been updated")
            return redirect("%s?with=&id=%s" % (reverse('cpanel.EditCourseWith'), request.GET.get('id')))

    return render(request, "cpanel_view/with/edit-with.html", {'course': course, 'form': fm})


@role_required(allowed_roles=["admin"])
def CloneCourseWith(request):
    if request.GET.get('with') == "country":
        return CloneCourseWithCountry(request)
    elif request.GET.get('with') == "city":
        return CloneCourseWithCity(request)
    else:
        return CloneCourseWithOut(request)


def CloneCourseWithCountry(request):
    course = WithCountry.objects.get(pk=request.GET.get('id'))

    fm = WithCountryEditForm()

    fm.fields['course'].initial = course.course
    fm.fields['description'].initial = course.description
    fm.fields['features'].initial = course.features
    fm.fields['learn'].initial = course.learn
    fm.fields['syllabus'].initial = course.syllabus
    fm.fields['scheduled_dates'].initial = course.scheduled_dates
    fm.fields['scheduled_times'].initial = course.scheduled_times
    fm.fields['country'].initial = course.country
    fm.fields['course_language'].initial = course.course_language
    fm.fields['currency'].initial = course.currency
    fm.fields['course_amount'].initial = course.course_amount


    if request.method == 'POST':

        fm = WithCountryEditForm(request.POST)
        if fm.is_valid():
            wc = WithCountry()
            wc.course = fm.cleaned_data['course']
            wc.description = fm.cleaned_data['description']
            wc.features = fm.cleaned_data['features']
            wc.learn = fm.cleaned_data['learn']
            wc.syllabus = fm.cleaned_data['syllabus']
            wc.country = fm.cleaned_data['country']
            wc.scheduled_dates = fm.cleaned_data['scheduled_dates']
            wc.scheduled_times = fm.cleaned_data['scheduled_times']
            wc.course_language = fm.cleaned_data['course_language']
            wc.currency = fm.cleaned_data['currency']
            wc.course_amount = fm.cleaned_data['course_amount']
            wc.save()
            messages.success(request, "Course has been Added")
            return redirect("%s?with=country&id=%s" % (reverse('cpanel.CloneCourseWith'), request.GET.get('id')))
    return render(request, "cpanel_view/with/edit-with.html", {'course': course, 'form': fm})

def CloneCourseWithCity(request):
    course = WithCity.objects.get(pk=request.GET.get('id'))

    fm = WithCityFormEdit()

    fm.fields['course'].initial = course.course
    fm.fields['description'].initial = course.description
    fm.fields['features'].initial = course.features
    fm.fields['learn'].initial = course.learn
    fm.fields['syllabus'].initial = course.syllabus
    fm.fields['scheduled_dates'].initial = course.scheduled_dates
    fm.fields['scheduled_times'].initial = course.scheduled_times
    fm.fields['city'].initial = course.city
    fm.fields['country'].initial = course.country
    fm.fields['course_language'].initial = course.course_language
    fm.fields['currency'].initial = course.currency
    fm.fields['course_amount'].initial = course.course_amount

    if request.method == 'POST':
        fm = WithCityFormEdit(request.POST)
        if fm.is_valid():
            wc = WithCity()
            wc.course = fm.cleaned_data['course']
            wc.description = fm.cleaned_data['description']
            wc.features = fm.cleaned_data['features']
            wc.learn = fm.cleaned_data['learn']
            wc.syllabus = fm.cleaned_data['syllabus']
            wc.city = fm.cleaned_data['city']
            wc.country = fm.cleaned_data['country']
            wc.scheduled_dates = fm.cleaned_data['scheduled_dates']
            wc.scheduled_times = fm.cleaned_data['scheduled_times']
            wc.course_language = fm.cleaned_data['course_language']
            wc.currency = fm.cleaned_data['currency']
            wc.course_amount = fm.cleaned_data['course_amount']
            wc.save()
            messages.success(request, "Course has been Added")
            return redirect("%s?with=city&id=%s" % (reverse('cpanel.CloneCourseWith'), request.GET.get('id')))
    return render(request, "cpanel_view/with/edit-with.html", {'course': course, 'form': fm})

def CloneCourseWithOut(request):
    course = WithOutCountryCity.objects.get(pk=request.GET.get('id'))

    fm = WithoutCityCountryForm()

    fm.fields['course'].initial = course.course
    fm.fields['description'].initial = course.description
    fm.fields['features'].initial = course.features
    fm.fields['learn'].initial = course.learn
    fm.fields['syllabus'].initial = course.syllabus
    fm.fields['scheduled_dates'].initial = course.scheduled_dates
    fm.fields['scheduled_times'].initial = course.scheduled_times
    fm.fields['course_language'].initial = course.course_language
    fm.fields['currency'].initial = course.currency
    fm.fields['course_amount'].initial = course.course_amount

    if request.method == 'POST':
        fm = WithoutCityCountryForm(request.POST)
        if fm.is_valid():
            wc = WithOutCountryCity()
            wc.course = fm.cleaned_data['course']
            wc.description = fm.cleaned_data['description']
            wc.features = fm.cleaned_data['features']
            wc.learn = fm.cleaned_data['learn']
            wc.syllabus = fm.cleaned_data['syllabus']
            wc.scheduled_dates = fm.cleaned_data['scheduled_dates']
            wc.scheduled_times = fm.cleaned_data['scheduled_times']
            wc.course_language = fm.cleaned_data['course_language']
            wc.currency = fm.cleaned_data['currency']
            wc.course_amount = fm.cleaned_data['course_amount']
            wc.save()
            messages.success(request, "Course has been Added")
            return redirect("%s?with=&id=%s" % (reverse('cpanel.CloneCourseWith'), request.GET.get('id')))

    return render(request, "cpanel_view/with/edit-with.html", {'course': course, 'form': fm})


def AddFaq(request):
    fm = AddFAQ()
    if request.method == "POST":
        fm = AddFAQ(request.POST)
        if fm.is_valid():
            f = Faq()
            f.course = fm.cleaned_data['course']
            f.question = fm.cleaned_data['question']
            f.answer = fm.cleaned_data['answer']
            f.save()
            messages.success(request,"Question was successfully added to FAQ list")
            return redirect(reverse('cpanel.AddFaq'))
    return render(request,'cpanel_view/FAQ/add.html',{'form': fm})

def EditFaq(request):
    faq = Faq.objects.all()
    return render(request,'cpanel_view/FAQ/list.html',{'faq':faq})


def UpdateFaq(request):
    f = Faq.objects.get(pk=request.GET.get('id'))
    fm = AddFAQ()
    fm.fields['course'].initial = f.course
    fm.fields['question'].initial = f.question
    fm.fields['answer'].initial = f.answer
    if request.method == "POST":
        fm = AddFAQ(request.POST)
        if fm.is_valid():
            f.course = fm.cleaned_data['course']
            f.question = fm.cleaned_data['question']
            f.answer = fm.cleaned_data['answer']
            f.save()
            messages.success(request,"Question was successfully Updated")
            return redirect("%s?id=%s"%(reverse('cpanel.UpdateFaq'),request.GET.get('id')))
    return render(request,'cpanel_view/FAQ/add.html',{'form': fm})

def deleteFaq(request):
    faq = Faq.objects.get(pk=request.GET.get('id'))
    faq.delete()
    messages.error(request,"Question was successfully deleted")
    return redirect(reverse('cpanel.EditFaq'))


def getCoutryDetail(request):
    if request.GET.get('q') == 'c':
        data = list(CountryList.objects.values_list('country_code','country_name'))
        return JsonResponse(data,safe=False)
    else:
        data = list(CityList.objects.all().values_list('city_name').filter(country_code=request.GET.get('c')))
        return JsonResponse(data, safe=False)

def getCityDetail(request):
    data = list(CityList.objects.filter(country_code=request.GET.get('q')).values_list('city_name','country_code'))
    return JsonResponse(data,safe=False)

def getCourseList(request):
    data = list(Course.objects.values_list('title'))
    return JsonResponse(data,safe=False)


class TestUpload(View):

    def get(self, request):
        return render(request,"test.html")

    def post(self, request):
        upload_path = save_to(request,"course","mypic")
        return HttpResponse(upload_path)
