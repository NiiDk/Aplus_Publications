from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.AcademicLoginView.as_view(), name='login'),
    path('logout/', views.AcademicLogoutView.as_view(), name='logout'),
    path('register/', views.StudentRegistrationView.as_view(), name='register'),
]
