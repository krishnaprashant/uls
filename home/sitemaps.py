from django.contrib import sitemaps
from django.urls import reverse
from .models import Snippet, Course

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return []

    def location(self, item):
        return reverse(item)


class SnippetSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Course.objects.all()

class CourseSnippetSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Course.objects.all()

    def location(self, item, country):
        return reverse('get_course_details',kwargs={'slug':item.slug})
