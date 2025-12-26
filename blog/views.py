from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Category

class PostListView(ListView):
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED)
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'blog/post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED)

def post_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category, status=Post.Status.PUBLISHED)
    return render(request, 'blog/post_list.html', {
        'category': category,
        'posts': posts,
        'categories': Category.objects.all()
    })
