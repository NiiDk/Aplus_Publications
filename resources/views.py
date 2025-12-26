from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.http import HttpResponse
from .models import Resource, ResourceDownload

class ResourceListView(ListView):
    model = Resource
    template_name = 'resources/resource_list.html'
    context_object_name = 'resources'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        resource_type = self.request.GET.get('type')
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)
        return queryset

def resource_download(request, slug):
    resource = get_object_or_404(Resource, slug=slug)
    
    # Simple Download Tracking
    ResourceDownload.objects.create(
        resource=resource,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT')
    )
    
    # Increment counter
    resource.download_count += 1
    resource.save(update_fields=['download_count'])
    
    return redirect(resource.file.url)
