from django.urls import path, include
from .views import AddEvent, Blog, ListBlog, ListEvents, UpdateBlog, AddCourse, ListCourse, UpdateCourse, UpdateEvent, AddTraining, AddTraining, UpdateTraining, ListTrainings, TestUpload
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.home), name="AdminHome"),
    path('get-enrolled',login_required(views.get_enrolled),name="cpanel.get_enrolled"),
    path('login', views.cpanel_login, name="cpanel_login"),

    #blog
    path('blog/', login_required(Blog.as_view()), name="Blog"),
    path('list-blog/', login_required(ListBlog.as_view()), name="ListBlog"),
    path('blog-update/', login_required(UpdateBlog.as_view()), name="UpdateBlogForm"),
    path('blog/delete', login_required(views.delete_blog), name="DeleteBlog"),

    #course
    path('course/add/', login_required(AddCourse.as_view()), name="AddCourse"),
    path('course/list/', login_required(ListCourse.as_view()), name="ListCourse"),
    path('course/update/', login_required(UpdateCourse.as_view()), name="UpdateCourseForm"),
    path('course/delete/', login_required(views.delete_course), name="DeleteCourse"),

    #event
    path('event/add/', login_required(AddEvent.as_view()), name="AddEvent"),
    path('event/list/', login_required(ListEvents.as_view()), name="ListEvents"),
    path('event/update/', login_required(UpdateEvent.as_view()), name="UpdateEventForm"),
    path('event/delete/', login_required(views.delete_event), name="DeleteEvent"),

    #event
    path('training/add/', login_required(AddTraining.as_view()), name="AddTraining"),
    path('training/list/', login_required(ListTrainings.as_view()), name="ListTrainings"),
    path('training/update/', login_required(UpdateTraining.as_view()), name="UpdateTrainingForm"),
    path('training/delete/', login_required(views.delete_training), name="DeleteTraining"),

    path('section/add/',login_required(views.AddSection),name='cpanel.AddSection'),
    path('section/edit/',login_required(views.EditSection),name='cpanel.EditSection'),
    path('section/update/',login_required(views.UpdateSection),name='cpanel.UpdateSection'),
    path('section/delete/',login_required(views.DeleteSection),name='cpanel.DeleteSection'),


    path('content/add/',login_required(views.AddContent),name='cpanel.AddContent'),
    path('content/edit/',login_required(views.EditContent),name='cpanel.EditContent'),
    path('content/update/',login_required(views.UpdateContent),name='cpanel.UpdateContent'),
    path('content/delete/',login_required(views.DeleteContent),name='cpanel.DeleteContent'),

    #url based content
    path('content/custom/add/',login_required(views.AddCustomContent),name='cpanel.AddCustomContent'),
    path('content/custom/edit/',login_required(views.EditCustomContent),name='cpanel.EditCustomContent'),
    path('content/custom/update/',login_required(views.UpdateCustomContent),name='cpanel.UpdateCustomContent'),
    path('content/custom/delete/',login_required(views.DeleteCustomContent),name='cpanel.DeleteCustomContent'),

    path('course/add/with/',login_required(views.AddCourseWith),name="cpanel.AddCourseWith"),
    path('course/add/title/', login_required(views.AddTitle), name="cpanel.AddTitle"),
    path('course/delete/title/', login_required(views.DeleteTitle),name="cpanel.DeleteTitle"),
    path('course/delete/with/', login_required(views.DeleteCourseWith),name="cpanel.DeleteCourseWith"),
    path('course/Edit/with/', login_required(views.EditCourseWith),name="cpanel.EditCourseWith"),
    path('course/clone/with/', login_required(views.CloneCourseWith),name="cpanel.CloneCourseWith"),
    #test upload


    #Faq
    path('faq/add/',login_required(views.AddFaq),name="cpanel.AddFaq"),
    path('faq/edit/',login_required(views.EditFaq),name="cpanel.EditFaq"),
    path('faq/update/',login_required(views.UpdateFaq),name="cpanel.UpdateFaq"),
    path('faq/delete/',login_required(views.deleteFaq),name="cpanel.deleteFaq"),

    path('country/details/', views.getCoutryDetail, name="CountryDetails"),
    path('city/details/', views.getCityDetail, name="CityDetail"),
    path('course/list/json', views.getCourseList, name="CourselistJson"),
    path('test-upload',TestUpload.as_view(),name="test_upload"),
]
