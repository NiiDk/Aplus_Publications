from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .sitemaps import TextbookSitemap, PostSitemap, PageSitemap

sitemaps = {
    'textbooks': TextbookSitemap,
    'posts': PostSitemap,
    'pages': PageSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('shop/', include('shop.urls', namespace='shop')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('resources/', include('resources.urls', namespace='resources')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('news/', include('news.urls', namespace='news')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('', include('pages.urls', namespace='pages')),
    
    # SEO
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
