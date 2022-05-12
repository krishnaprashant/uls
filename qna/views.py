from django.shortcuts import redirect,  render
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.db.utils import OperationalError
from .models import Qna,Comments
from cpanel.models import Content,Section
# Create your views here.


def home(request):
    content = str(object='')
    try:
        section = Section.objects.get(pk=1)
        content = section.content.content
    except:
        pass
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request,'User has to login for commenting')
            return redirect(reverse('qna_home'))
        if request.user.usertype == "admin":
            messages.error(request,"Unfortunately you don't have enough permissions to perform this task.")
            return redirect(reverse('qna_home'))
        query = request.POST.get('query')
        if query == "" or query is None:
            if 'pst' in request.POST:
                id = request.POST.get('pst')
                p = Qna.objects.get(pk=id)
                p.delete()
                messages.success(request,"Your post was successfully.")
                return redirect(reverse('qna_home'))
            messages.error(request,"Please enter some thing")
            return redirect(reverse('qna_home'))
        else:
            try:
                Qna.objects.create(user_id=request.user.id,post=query)
                messages.success(request,'commented')
                return redirect(reverse('qna_home'))
            except OperationalError:
                messages.error(request,"Emojies are not supported")
                return redirect(reverse('qna_home'))

    posts = Qna.objects.all().order_by('-id')
    return render(request,'qna.html',{'posts':posts,'content':content})


def post_thread(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request,'User has to login for commenting')
            return redirect("%s?id=%s"%(reverse('qna_thread'),request.GET.get('id')))
        if request.user.usertype == "admin":
            messages.error(request,"Unfortunately you don't have enough permissions to perform this task.")
            return redirect("%s?id=%s"%(reverse('qna_thread'),request.GET.get('id')))
        query = request.POST.get('comment')
        if query == "" or query is None:
            if 'cmt' in request.POST:
                id = request.POST.get('cmt');
                c = Comments.objects.get(pk=id);
                c.delete()
                messages.success(request,"Your comment was successfully")
                return redirect("%s?id=%s"%(reverse('qna_thread'),request.GET.get('id')))
            messages.error(request,"Please enter some thing")
            return redirect("%s?id=%s"%(reverse('qna_thread'),request.GET.get('id')))
        else:
            Comments.objects.create(user_id=request.user.id,qna_id=request.GET.get('id'),comment=request.POST.get('comment'))
    posts = Qna.objects.get(pk=request.GET.get('id'))
    comments = Comments.objects.filter(qna_id=request.GET.get('id'))
    return render(request,'qna_thread.html',{'posts':posts,'comments':comments})
