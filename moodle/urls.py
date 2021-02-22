from django.urls import path
from . import views

from django.urls import path

from . import views

app_name = 'moodle'
urlpatterns = [
    path('', views.index, name='index'),
]
