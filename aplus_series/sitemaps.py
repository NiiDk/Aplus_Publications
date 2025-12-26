from django.contrib.sitemaps import Sitemap
from shop.models import Textbook
from blog.models import Post
from pages.models import Page

class TextbookSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Textbook.objects.all()

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Post.objects.filter(status='PB')

class PageSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Page.objects.filter(is_active=True)
