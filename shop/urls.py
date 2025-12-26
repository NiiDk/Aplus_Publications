from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.TextbookListView.as_view(), name='textbook_list'),
    path('<slug:slug>/', views.TextbookDetailView.as_view(), name='textbook_detail'),
]
