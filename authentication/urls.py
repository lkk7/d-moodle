from django.contrib.auth import views
from .views import register
from django.urls import path


app_name = 'authentication'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='authentication:login'),
         name='logout'),
    path('register/', register, name='register'),
]
