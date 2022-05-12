from django.urls import path, include
from .sitemaps import StaticViewSitemap, SnippetSitemap, CourseSnippetSitemap
from . import views
from home.views import Register,Login
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap

sitemaps = {
'static' : StaticViewSitemap,
'snippet':SnippetSitemap
}
courseSitemaps = {
'CourseSnippetSitemap':CourseSnippetSitemap,
}

urlpatterns = [    
    path('sitemap.xml',sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path("<str:country>/<str:country_name>-sitemap.xml", views.CustomSiteMapCountry, name="CustomSiteMapCountry"),
    path("sitemap-sitemap.xml", views.HomeSiteMap, name="HomeSiteMap"),
    path('',views.home,name="homepage"),
    path('register/', Register.as_view(),name="register"),
    path('login/', Login.as_view() ,name="login"),
    path('accounts/login/', Login.as_view() ,name="login"),
    path('logout/', views.logout_request ,name="logout"),
    path('register/enroll/', views.enroll ,name="register.enroll"),
    path('register/training/enroll/', views.training_enroll ,name="register.training.enroll"),
    path('register/enrolled/', views.enrolled, name="register.enrolled"),
    path('register/training/enrolled/', views.training_enrolled, name="register.training.enrolled"),
    path('details/enrolled/<type>', views.enrolled_details, name="details.enrolled"),
    path('user/details/', views.user_details, name="home.profile"),
    path('contactus',views.contactus, name="home.contactus"),
    path('about',views.AboutUs, name="home.AboutUs"),
    path('partner-program', views.PartnerProgramme, name="home.PartnerProgramme"),
    path('terms-and-condition',views.TermsAndCondition, name="home.TermsAndCondition"),
    path('privacy-policy',views.PrivacyPolicy, name="home.PrivacyPolicy"),
    path('refund-policy', views.RefundPolicy, name="home.RefundPolicy"),
    path('rescheduling-policy', views.ReschedulingPolicy, name="home.ReschedulingPolicy"),
    path('set-country/<str:country>',views.set_country,name="home.set_country"),
    path('set-city/<str:slug>/<str:city>',views.set_city,name="home.set_city"),
    path('acknoledgement',views.acknowledgement,name="home.acknowledgement"),

    # reset password start
    path('reset-password', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset-password-sent', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset-password/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset-password-complete', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    # reset password ends

    #ajax
    path('get/title/details',views.getTitleDetails,name="home.getTitleDetails"),

    #fraud
    path('fraud',views.fraud,name="home.fraud"),

    #error
    path("error-page",views.ErrorPage,name="error"),

    #static pages below
    path('<country>', views.country,name="coutryHomepage"),
    path('in/allcourses/project-management', views.project_management,name="in.project_management"),
    path('in/project-management/<str:slug>', views.get_course_details,name="in.get_course_details.slug"),
    path('test/', views.test, name="home.test"),
    path('snippet/<slug:slug>',views.snippet_detail)
]
