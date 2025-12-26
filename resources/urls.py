from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    path('', views.ResourceListView.as_view(), name='resource_list'),
    path('download/<slug:slug>/', views.resource_download, name='resource_download'),
]
