from django.shortcuts import render
from .models import Events
from django.core.paginator import Paginator


# Create your views here.
def list_events(request):
    page_number = request.GET.get('page')
    events = Events.objects.all()
    events = Paginator(events, 3)
    onset = (int(page_number) * 3 ) - 3
    offset = int(page_number) *  3
    string_slice = f"{onset}:{offset}"
    page_number = int(page_number)
    return render(request,'events.html',{'events':events,"string_slice":string_slice,"page_number":page_number})
