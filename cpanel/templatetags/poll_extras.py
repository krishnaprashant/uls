from django import template
import json
import datetime
import base64
from datetime import datetime
import calendar
import re

register = template.Library()


@register.filter(name='split')
def split(value, arg):
    return value.split(arg)


@register.filter(name='loadjson')
def loadjson(data):
    if data:
        data = data.replace("'",'"')
        data = json.loads(data)
        return data
    else:
        return data

@register.filter(name='CheckElementInString')
def CheckElementInString(value, arg):
    if arg in value.split(","):
        return True
    else:
        return False

@register.filter(name='prev')
def prev(value):
    return (int(value) * 3)-2

@register.filter(name='nxt')
def nxt(value):
    return int(value) * 3


@register.filter(name='changeEncoding')
def changeEncoding(txt):

    if "<" in txt:
        return txt
    else:
        return base64.b64decode(removeUTF(txt)).decode()


@register.filter(name='removeUTF')
def removeUTF(txt):
    s = txt.replace("b'","")
    return s.replace("'","")

def print_timestamp(timestamp):
    ts = str(timestamp)
    ts = ts[:-3]
    ts = int(ts)
    return str(datetime.datetime.fromtimestamp(ts))


@register.filter(name="ExtractYear")
def ExtractYear(txt):
    my = txt.split(';')[0]
    return my.split('|')[-1]

@register.filter(name="ExtractMonth")
def ExtractMonth(txt):
    my = txt.split(';')[0]
    return my.split('|')[0]


@register.filter(name="ExtractDates")
def ExtractDates(txt):
    try:
        t = txt.split(';')[-1]
        my = txt.split(';')[0]
        m = my.split(',')[0].split('|')[0]
        y = my.split(',')[-1].split('|')[-1]
        c = t.split(',')
        h = ""
        for i in c:
            h += '<div class="col-md-2 text-center p-0 pt-3 pb-3 me-2 ms-2 mt-1 mb-1 border"><div class="border-bottom">%s</div><div>%s</div></div>' % (i,converToDay(m,i,y))
        return h
    except:
        return "<p>Dates are not entered in correct format</p>"

def converToDay(m,d,y):
    datetime_object = datetime.strptime('%s %s %s'%(m,d,y), '%b %d %Y')
    return calendar.day_name[datetime_object.weekday()].upper()[:3]


@register.filter(name="setdynamicvalue")
def setdynamicvalue(txt,arg):

    regex = r'(?<=\{{).*?(?=\}})'
    op = re.sub(regex, arg, txt)
    return op.replace("{{", "").replace("}}", "")



register.filter('ExtractYear', ExtractYear)

register.filter('ExtractMonth', ExtractMonth)

register.filter('ExtractDates', ExtractDates)

register.filter('print_timestamp', print_timestamp)

register.filter('prev', prev)

register.filter('changeEncoding', changeEncoding)

register.filter('nxt', nxt)

register.filter('split',split)

register.filter('loadjson',loadjson)
register.filter('removeUTF',removeUTF)
