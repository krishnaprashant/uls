from django.test import TestCase
from .models import Qna
from .views import home

# Create your tests here.

class QNATestCase(TestCase):

    def testLoggedIn(self):
        pass

    def AddComment(self):
        p = Qna.objects.get(pk=20)
        p.user.add(4,through_defaults={'comment':'test comment'})
