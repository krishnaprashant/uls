from django import template
from datetime import datetime

from home.models import Course

register = template.Library()


@register.filter(name="listCourse")
def listCourse(enrollment):
    c = 0
    course_list = ""
    for i in enrollment:
        c += 1
        course = getcoursebyid(i['course_id'])
        course_list += '''
            <li class="single-lessons">
            <div class="d-md-flex d-lg-flex align-items-center">
                <span class="number">%s.</span>
                <a href="/course/%s" class="lessons-title">%s</a>
                <a href="/course/%s"><span class="preview">view Details</span></a>
            </div>
            <div class="lessons-info">
                <span class="duration" data-bs-toggle="tooltip" data-placement="top" title="Duration"><i class='bx bx-chalkboard'></i>%s</span>
            </div>
            </li>                      
            ''' % (c, course['slug'], course['title'], course['slug'], course['category'])
    
    return course_list

def getcoursebyid(id):
    course = Course.objects.all().values('id', 'title', 'slug','category')
    for i in course:
        if i['id'] == id:
            return i


register.filter('listCourse', listCourse)
