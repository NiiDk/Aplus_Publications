from django.views.generic import ListView
from .models import NewsAnnouncement

class NewsListView(ListView):
    model = NewsAnnouncement
    template_name = 'news/news_list.html'
    context_object_name = 'announcements'
    
    def get_queryset(self):
        return NewsAnnouncement.objects.filter(is_published=True).order_by('-priority', '-scheduled_at')
