import random
from django.http import HttpResponse
import json
import string

def pprint(data):
    return HttpResponse(f"<pre>{json.dumps(data,indent=4)}</pre>")


def create_new_ref_number():
     return str(random.randint(1000, 9999))

def create_ticket():
    S = 10  # number of characters in the string.    
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
    return str(ran)
