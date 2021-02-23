from django.urls import path
from . import views

from django.urls import path

from . import views

app_name = 'moodle'
urlpatterns = [
    path('', views.index, name='index'),
    path('lesson/list/', views.LessonListView.as_view(),
         name='lesson_list'),
    path('lesson/<int:pk>/', views.LessonDetailView.as_view(),
         name='lesson_view'),
    path('course/list/', views.CourseListView.as_view(),
         name='lesson_list'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(),
         name='course_view')
]
