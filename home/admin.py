from django.contrib import admin
from .models import User, Faq
from .models import Course, Enrollment, Training, TrainingEnrollment, WithCountry, WithCity, WithOutCountryCity, CourseTitle, EnrollmentWithCountry, EnrollmentWithCity, EnrollmentWithOut, ErrorLog, CountryList, CityList, Snippet
# Register your models here.



admin.site.register(Course)
admin.site.register(User)
admin.site.register(Enrollment)
admin.site.register(Training)
admin.site.register(TrainingEnrollment)
admin.site.register(WithCountry)
admin.site.register(WithCity)
admin.site.register(WithOutCountryCity)
admin.site.register(CourseTitle)
admin.site.register(EnrollmentWithCountry)
admin.site.register(EnrollmentWithCity)
admin.site.register(EnrollmentWithOut)
admin.site.register(ErrorLog)
admin.site.register(Faq)
admin.site.register(CountryList)
admin.site.register(CityList)
admin.site.register(Snippet)
