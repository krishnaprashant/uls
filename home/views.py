from django.http.response import JsonResponse
import helpers
import django
from django.contrib import auth
from django.contrib.auth import logout
from django.shortcuts import redirect, render, get_object_or_404
from django.http import request, HttpResponse
from django.views import View
from helpers.basic import pprint
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib import messages
from home.forms import LoginForm, RegisterForm
from common import form_errors_helper
from home.models import Training
from home.models import Course, Enrollment, TrainingEnrollment, CourseTitle, CountryList
import json
from django.db import IntegrityError
from django.forms.models import model_to_dict
from .models import CourseTitle, EnrollmentWithCity, EnrollmentWithCountry, EnrollmentWithOut, ErrorLog, User, WithCity, WithCountry, WithOutCountryCity, Snippet, CityList
from datetime import date
import datetime
from django.core.files.storage import FileSystemStorage
from cpanel.models import Content,Section
from django.core.mail import send_mail
from django.conf import settings
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from ast import literal_eval
from itertools import chain



def home(request):

    training = Training.objects.all()
    course = Course.objects.all()
    content = str(object='')
    try:
        section = Section.objects.get(pk=1)
        content = section.content.content
    except:
        pass
    return render(request, "index.html",{
    'training':training,
    'course' : course,
    'content':content
    })

def country(request,country):
    training = Training.objects.all()
    course = Course.objects.all()
    content = str(object='')
    try:
        section = Section.objects.get(pk=1)
        content = section.content.content
    except:
        pass
    return render(request, "index.html",{
    'training':training,
    'course' : course,
    'content':content,
    'country':country
    })


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect(reverse("login"))

class Register(View):
    def get(self,request):
        content = str(object='')
        try:
            section = Section.objects.get(pk=1)
            content = section.content.content
        except:
            pass
        return render(request, "register.html",{'content':content})

    def post(self,request,*args,**kwargs):
        rf = RegisterForm(request.POST)
        if not rf.is_valid():
            content = str(object='')
            try:
                section = Section.objects.get(pk=1)
                content = section.content.content
            except:
                pass

            return render(request, "register.html",{'content':content, 'form':rf})
        try:
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            password = request.POST.get('password')
            User = get_user_model()
            user = User.objects.create_user(username=email, first_name=first_name, last_name=last_name, email=email, phone=phone, password=password,usertype="user")
            user.save()
            messages.info(request,'User is registered')
            return redirect(reverse('register'))
        except IntegrityError as e:
            messages.info(request,"User already exist")
            return redirect(reverse('register'))

class Login(View):

    def get(self,request):
        content = str(object='')
        try:
            section = Section.objects.get(pk=1)
            content = section.content.content
        except:
            pass
        return render(request,'login.html',{'content':content})

    def post(self,request):
        lf = LoginForm(request.POST)
        if not lf.is_valid():
            messages.error(request,'inputs are required')
            return redirect("%s?next=%s"%(reverse('login'),request.GET.get('next')))
        User = get_user_model()
        email = request.POST.get('email')
        password = request.POST.get('password')
        # return HttpResponse(json.dumps(request.POST,indent=1))
        user = auth.authenticate(username=email, password=password)

        if user is not None:
            auth.login(request,user)
            quantity = 1
            if 'quantity' in request.session:
                quantity = request.session['quantity']
            if 'course_id' in request.session:
                id = request.session['course_id']
                return redirect("%s?type=course&id=%s&quantity=%s"%(reverse('PUM.Home'),id,quantity))
            if 'training_id' in request.session:
                id = request.session['training_id']
                return redirect("%s?type=training&id=%s&quantity=%s"%(reverse('PUM.Home'),id,quantity))
            if request.GET.get('next') is not None:
                return redirect(request.GET.get('next'))
            return redirect(reverse("homepage"))
        else:
            messages.info(request,'invalid credentials')
            return redirect("%s?next=%s"%(reverse('login'),request.GET.get('next')))




def enroll(request):
    id = request.GET.get('id')
    quantity = request.GET.get('quantity')
    code = request.GET.get('code')
    with_ = ""
    a = WithCountry.objects.filter(pk=id,course_code=code).count()
    b = WithCity.objects.filter(pk=id,course_code=code).count()
    c = WithOutCountryCity.objects.filter(pk=id, course_code=code).count()

    if a > 0:
        with_ = "country"
        x = EnrollmentWithCountry.objects.filter(user_id=request.user.id,with_country=id).count()
        if x > 0:
            messages.error(request,"Already registered for this course")
            return redirect(reverse("home.profile"))
    elif b > 0:
        with_ = "city"
        y = EnrollmentWithCity.objects.filter(user_id=request.user.id, with_city=id).count()
        if y > 0:
            messages.error(request,"Already registered for this course")
            return redirect(reverse("home.profile"))
    elif c > 0:
        with_= ""
        z = EnrollmentWithOut.objects.filter(user_id=request.user.id, with_out=id).count()
        if z > 0:
            messages.error(request,"Already registered for this course")
            return redirect(reverse("home.profile"))

    if request.user.is_authenticated:
        request.session['course_id'] = id
        return redirect("%s?type=course&id=%s&quantity=%s&with=%s" % (reverse('PUM.Home'), id, request.GET.get('quantity'), with_))
    else:
        request.session['course_id'] = id
        request.session['quantity'] = request.GET.get('quantity')
        return redirect(reverse('register'))


def enrolled(request,res):
    wth = literal_eval(res["productinfo"])["wth"]
    if wth == "country":
        enroll_with_country(res)
    elif wth == "city":
        enroll_with_city(res)
    else:
        enroll_with_out(res)
    url = reverse('details.enrolled',kwargs={'type':'country'})
    return redirect(f"{url}?id={res['id']}")


def enroll_with_country(res):
    today = date.today()
    user_id = User.objects.get(email=res['email'])
    date_enrolled = today.strftime("%Y-%m-%d")
    course_id = res['id']
    status = res['status']
    txnid = res['txnid']
    amount = res['amount']
    withCountry = WithCountry.objects.get(pk=course_id)
    EnrollmentWithCountry.objects.create(
        user = user_id,
        with_country = withCountry,
        date_enrolled=date_enrolled,
        status = status,
        txnid = txnid,
        amount = int(float(amount))
    )
    return

def enroll_with_city(res):
    today = date.today()
    user_id = User.objects.get(email=res['email'])
    date_enrolled = today.strftime("%Y-%m-%d")
    course_id = res['id']
    status = res['status']
    txnid = res['txnid']
    amount = res['amount']
    withCity = WithCity.objects.get(pk=course_id)
    EnrollmentWithCity.objects.create(
        user=user_id,
        with_city=withCity,
        date_enrolled=date_enrolled,
        status=status,
        txnid=txnid,
        amount=int(float(amount))
    )
    return

def enroll_with_out(res):
    today = date.today()
    user_id = User.objects.get(email=res['email'])
    date_enrolled = today.strftime("%Y-%m-%d")
    course_id = res['id']
    status = res['status']
    txnid = res['txnid']
    amount = res['amount']
    without = WithOutCountryCity.objects.get(pk=course_id)
    EnrollmentWithOut.objects.create(
        user=user_id,
        with_out=without,
        date_enrolled=date_enrolled,
        status=status,
        txnid=txnid,
        amount=int(float(amount))
    )
    return



def training_enrolled(request,res):
    user_id = User.objects.get(email=res['email']).id
    today = date.today()
    # YY/mm/dd
    date_enrolled = today.strftime("%Y-%m-%d")
    training_id = res['id']
    already_exist = TrainingEnrollment.objects.filter(user_id=user_id,training_id=training_id).count()
    if already_exist > 0:
        url = reverse('details.enrolled',kwargs={'type':'already'})
        return redirect(url)
    user_id = user_id
    status = res['status']
    txnid = res['txnid']
    amount = res['amount']
    training = Training.objects.get(pk=training_id)
    training.user.add(user_id,through_defaults={'date_enrolled':date_enrolled,"status":status,"txnid":txnid,"amount":int(float(amount))})
    url = reverse('details.enrolled',kwargs={'type':'training'})
    return redirect(f"{url}?id={training_id}")



def training_enroll(request):
    id = request.GET.get('id')
    if request.user.is_authenticated:
        request.session['training_id'] = id
        return redirect("%s?type=training&id=%s"%(reverse('PUM.Home'),id))
    else:
        request.session['training_id'] = id
        return redirect(reverse('register'))

def save_to(request,path,file):
    pic = request.FILES.get(file)
    fs = FileSystemStorage()
    filename = fs.save(f"static//{path}//{pic.name}", pic)
    uploaded_file_url = fs.url(filename)
    return uploaded_file_url

def enrolled_details(request,type):
    enrollment = []
    print(request.user.id)
    if type == "country":
        enrollment = EnrollmentWithCountry.objects.filter(with_country_id=request.GET.get('id'), user_id=request.user.id)
    elif type == "city":
        pass
    else:
        pass
    already = False
    content = str(object='')
    try:
        section = Section.objects.get(pk=1)
        content = section.content.content
    except:
        pass

    return render(request,'enroll-acknoledgement.html',{'enrollment':enrollment,'already':already, 'type':type, 'content':content })


def user_details(request):
    if request.method == "POST":
        u = User.objects.get(pk=request.user.id)
        u.profile_pic = save_to(request,"profile","propic")
        u.save()
        messages.success(request,"Profile Picture changed")
        redirect(reverse('home.profile'))

    country_data = WithCountry.objects.filter(enrollmentwithcountry__in=EnrollmentWithCountry.objects.filter(user_id=request.user.id)).values('course_id')
    city_data = WithCity.objects.filter(enrollmentwithcity__in=EnrollmentWithCity.objects.filter(user_id=request.user.id)).values('course_id')
    data = WithOutCountryCity.objects.filter(enrollmentwithout__in=EnrollmentWithOut.objects.filter(user_id=request.user.id)).values('course_id')
    enrollment = list(chain(country_data, city_data,data))

    return render(request, "profile.html", {'enrollment': enrollment})

def test(request):
    q = ""
    if 'cc' in request.GET:
        q = request.GET.get('cc')
    cityList = CityList.objects.all().filter(country_code=q).values()
    return JsonResponse(list(cityList), safe=False)



def project_management(request):
    courses = Course.objects.all()
    training = Training.objects.all()
    return render(request,"in/corporate-courses.html",{
    'courses':courses,
    'training':training
    })



def get_course_details(request,slug):
    course = Course.objects.get(slug=slug);
    return render(request,'course-with-country.html',{'course':course})



def check_if_amount_paid(request):
    return HttpResponse("this method is to be implemented")

def set_country(request,country):
    request.session['country'] = country
    return redirect('/%s'%country)

def set_city(request,slug,city):
    request.session['city'] = city
    return redirect(reverse('get_course_details',kwargs={'country':request.session['country'],'slug':slug,'city':city}))


def contactus(request):

    if request.method == "POST":
        html_message = render_to_string('email/contact.html', {'message': request.POST})
        name = request.POST['name']
        email = settings.EMAIL_HOST_USER
        message = request.POST['message']
        phone = request.POST['phone']
        subject = request.POST['subject']
        send_mail(
            subject,
            html_message,
            "alen@ulearnsystems.com",
            ['prashantkrishna5@gmail.com'],
            fail_silently=False,
        )
        return redirect(reverse('home.contactus'))

    return render(request,'contactus.html')


def AboutUs(request):
    return render(request,"about.html")

def PartnerProgramme(reqeust):
    return render(reqeust,"partner-program.html")

def TermsAndCondition(request):
    return render(request,"terms-of-use.html")

def PrivacyPolicy(request):
    return render(request,"privacy-policy.html")

def RefundPolicy(request):
    return render(request,"refund-policy.html")


def ReschedulingPolicy(request):
    return render(request,"rescheduling-policy.html")


def getTitleDetails(request):
    category = request.GET.get('cat')
    courseTitle = CourseTitle.objects.all().values().filter(category=category)
    responseData = list(courseTitle)
    return JsonResponse(responseData, safe=False)

def fraud(request):
    return render(request,'fraud.html')

def ErrorPage(request):
    ticket = ErrorLog.objects.get(pk=request.GET.get('tid')).ticket_number
    return render(request,"error-page.html",{"ticket":ticket})


def acknowledgement(request):
    name = ""
    if "contactus" in request.POST:
        html_message = render_to_string('email/contact.html', {'message': request.POST})
        name = request.POST['name']
        email = settings.EMAIL_HOST_USER
        message = request.POST['message']
        phone = request.POST['phone']
        subject = request.POST['subject']
        send_mail(
            subject,
            html_message,
            "training@ulearnsystems.com",
            ['prashantkrishna5@gmail.com'],
            fail_silently=False,
        )
        return redirect(reverse('home.acknowledgement'))
    return render(request,"acknowledgement.html")


def snippet_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    return HttpResponse(reverse('get_course_details',kwargs={'slug':slug}))


def CustomSiteMapCountry(request,country,country_name):
    # return JsonResponse(list(Course.objects.all().values('slug')),safe=False)
    courselist = Course.objects.all().values('slug')
    cityList = CityList.objects.all().filter(country_code=country).values('city_name')
    lastmod = datetime.datetime.now();
    changefreq = "daily"
    priority = 0.9
    return render(request,'custom_sitemap.xml',{'courselist':courselist, 'cityList':cityList, 'lastmod':lastmod,'changefreq':changefreq,'priority':priority, "country":country}, content_type="application/xhtml+xml" );


def HomeSiteMap(request):
    # return JsonResponse(list(CountryList.objects.all().values('country_name','country_code')),safe=False)
    countrylist = CountryList.objects.all().values('country_name','country_code')
    lastmod = datetime.datetime.now();
    changefreq = "daily"
    priority = 0.5
    return render(request,'sitemap_sitemap.xml',{'countrylist':countrylist,'lastmod':lastmod,'changefreq':changefreq,'priority':priority}, content_type="application/xhtml+xml" );
