from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Textbook, Subject, AcademicLevel
from .ai_integration import AcademicAIService

class TextbookListView(ListView):
    model = Textbook
    context_object_name = 'textbooks'
    paginate_by = 12

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['shop/partials/textbook_list_results.html']
        return ['shop/textbook_list.html']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Search
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(title__icontains=q) | queryset.filter(isbn__icontains=q)
            
        # Filters
        level = self.request.GET.get('level')
        if level:
            queryset = queryset.filter(academic_level__slug=level)
            
        subject = self.request.GET.get('subject')
        if subject:
            queryset = queryset.filter(subject__slug=subject)
            
        book_type = self.request.GET.get('type')
        if book_type:
            queryset = queryset.filter(book_type=book_type)
            
        return queryset.select_related('subject', 'academic_level')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['levels'] = AcademicLevel.objects.all()
        context['subjects'] = Subject.objects.all()
        context['book_types'] = Textbook.BookType.choices
        context['low_data_mode'] = self.request.GET.get('low_data') == 'true'
        return context

class TextbookDetailView(DetailView):
    model = Textbook
    template_name = 'shop/textbook_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Use our AI-ready service for recommendations
        context['recommendations'] = AcademicAIService.get_recommendations(
            user=self.request.user, 
            textbook=self.object
        )
        return context
