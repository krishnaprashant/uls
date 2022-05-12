from django.shortcuts import render
from django.http import HttpResponse
from home.models import Training
from home.models import Course, TrainingEnrollment
from cpanel.models import Content, Section
# Create your views here.


def home(request):
    content = str(object='')
    try:
        section = Section.objects.get(pk=1)
        content = section.content.content
    except:
        pass
    training = Training.objects.all()
    course = Course.objects.all()
    return render(request,'corporate-training.html',{
    'training':training,
    'course' : course,
    'content':content
    })


def details(request):
    id = request.GET.get('id')
    count = TrainingEnrollment.objects.filter(training_id=id,user_id=request.user.id).count()
    course = Training.objects.get(id=id)
    return render(request,"training-details.html",{"course":course,"count" : count})
