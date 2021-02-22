from django.urls import path
from . import views

from django.urls import path

from . import views

app_name = 'moodle'
urlpatterns = [
    path('', views.index, name='index'),
    path('lesson/<int:pk>/', views.LessonDetailView.as_view(),
         name='lesson_view')
]
