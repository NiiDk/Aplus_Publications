from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('category/<slug:category_slug>/', views.post_by_category, name='post_by_category'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]
