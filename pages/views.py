from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView, ListView
from .models import Page, FAQ, Enquiry
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.http import Http404
from django.contrib import messages

class HomeView(TemplateView):
    template_name = 'pages/home.html'

class PageDetailView(DetailView):
    model = Page
    template_name = 'pages/page_detail.html'
    context_object_name = 'page'

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        slug = self.kwargs.get(self.slug_url_kwarg)
        try:
            get_template(f"pages/{slug}.html")
        except TemplateDoesNotExist:
            if not self.object:
                raise Http404("Academic Page Not Found")
        
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_template_names(self):
        slug = self.kwargs.get(self.slug_url_kwarg)
        return [f"pages/{slug}.html", self.template_name]

class FAQListView(ListView):
    model = FAQ
    template_name = 'pages/faq.html'
    context_object_name = 'faqs'

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        role = request.POST.get('role')
        message = request.POST.get('message')
        
        if name and email and message:
            Enquiry.objects.create(
                name=name,
                email=email,
                role=role,
                message=message
            )
            messages.success(request, "Your academic enquiry has been received successfully.")
            return redirect('pages:contact')
            
    return render(request, 'pages/contact.html')

def about_view(request):
    try:
        page = Page.objects.get(slug='about-us')
        return render(request, 'pages/page_detail.html', {'page': page})
    except Page.DoesNotExist:
        return render(request, 'pages/about.html')
