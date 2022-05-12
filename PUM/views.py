from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, Template,RequestContext
import datetime
import hashlib
from random import randint
from django.urls.base import reverse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from home.models import Training, Course, WithCity, WithCountry, ErrorLog, WithOutCountryCity
from home.views import enrolled, training_enrolled
import json
from datetime import datetime as dt
import traceback

def Home(request):
	MERCHANT_KEY = "nfA8puCm"
	key="nfA8puCm"
	SALT = "89on0HeVJ3"
	PAYU_BASE_URL = "https://sandboxsecure.payu.in/_payment"
	action = ''
	posted={}
	amount = 0
	if request.GET.get('type') == "course":
		if request.GET.get('with') == "country":
			withCountry = WithCountry.objects.get(pk=request.GET.get('id'))
			amount = withCountry.course_amount * int(request.GET.get('quantity'))
			request.session['amount'] = amount
		elif request.GET.get('with') == "city":
			withCountry = WithCity.objects.get(pk=request.GET.get('id'))
			amount = withCountry.course_amount * int(request.GET.get('quantity'))
			request.session['amount'] = amount
		else:
			without = WithOutCountryCity.objects.get(pk=request.GET.get('id'))
			amount = without.course_amount * int(request.GET.get('quantity'))
			request.session['amount'] = amount
	else:
		training = Training.objects.get(id=request.GET.get('id'))
		amount = training.fee
	# Merchant Key and Salt provided y the PayU.
	for i in request.POST:
		posted[i]=request.POST[i]
	hash_object = hashlib.sha256(b'randint(0,20)')
	txnid=hash_object.hexdigest()[0:20]
	hashh = ''
	posted['txnid']=txnid
	hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
	posted['key']=key
	hash_string=''
	hashVarsSeq=hashSequence.split('|')
	for i in hashVarsSeq:
		try:
			hash_string+=str(posted[i])
		except Exception:
			hash_string+=''
		hash_string+='|'
	hash_string+=SALT
	hashh=hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
	action =PAYU_BASE_URL
	if(posted.get("key")!=None and posted.get("txnid")!=None and posted.get("productinfo")!=None and posted.get("firstname")!=None and posted.get("email")!=None):
		return render(request,'PUM/current_datetime.html',{"posted":posted,"hashh":hashh,"MERCHANT_KEY":MERCHANT_KEY,"txnid":txnid,"hash_string":hash_string,"action":action,"amount":amount })
	else:
		return render(request,'PUM/current_datetime.html',{"posted":posted,"hashh":"","MERCHANT_KEY":MERCHANT_KEY,"txnid":txnid,"hash_string":hash_string,"action":".","amount":amount })


@csrf_exempt
def success(request):
	try:
		status=request.POST.get("status")
		firstname=request.POST.get("firstname")
		amount=request.POST.get("amount")
		txnid=request.POST.get("txnid")
		posted_hash=request.POST.get("hash")
		key=request.POST.get("key")
		productinfo=request.POST.get("productinfo")
		email=request.POST.get("email")
		mobile=request.POST.get("mobile")
		salt="GQs7yium"
		try:
			additionalCharges=request.POST.get("additionalCharges")
			retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
		except Exception:
			retHashSeq = salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
		hashh=hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
		productinfo = "{"+productinfo+"}"
		res = productinfo.replace("'",'"')
		res = json.loads(res)
		pg_response = {"txnid":txnid,"status":status,"amount":amount,"productinfo":productinfo,"mobile":mobile,"email":email,"id":res['id']}
		if res['type'] == "course":
			return enrolled(request,pg_response)
		else:
			return training_enrolled(request,pg_response)
	except Exception as e:
		i = log_error(e)
		return redirect("%s?tid=%s"%(reverse("error"),i))


def log_error(err):
	i = ErrorLog.objects.create(
		error = err,
		ts= dt.now()
	)
	return i.pk


@csrf_exempt
def failure(request):
	status=request.POST.get("status")
	firstname=request.POST.get("firstname")
	amount=request.POST.get("amount")
	txnid=request.POST.get("txnid")
	posted_hash=request.POST.get("hash")
	key=request.POST.get("key")
	productinfo=request.POST.get("productinfo")
	email=request.POST.get("email")
	salt=""	
	try:
		additionalCharges=request.POST.get("additionalCharges")
		retHashSeq=str(additionalCharges)+'|'+str(salt)+'|'+str(status)+'|||||||||||'+str(email)+'|'+str(firstname)+'|'+str(productinfo)+'|'+str(amount)+'|'+str(txnid)+'|'+str(key)
	except Exception:
		retHashSeq = str(salt)+'|'+str(status)+'|||||||||||'+str(email)+'|'+str(firstname)+'|'+str(productinfo)+'|'+str(amount)+'|'+str(txnid)+'|'+str(key)
	hashh=hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
	if(hashh !=posted_hash):
		print ("Invalid Transaction. Please try again")
	else:
		print ("Thank You. Your order status is ", status)
		print ("Your Transaction ID for this transaction is ",txnid)
		print ("We have received a payment of Rs. ", amount ,". Your order will soon be shipped.")
	return render(request,"PUM/Failure.html",{'c':c})
