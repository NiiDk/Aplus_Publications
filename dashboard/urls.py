from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('user/', views.user_dashboard, name='user_hub'),
    path('admin-hub/', views.admin_dashboard, name='admin_hub'),
]
