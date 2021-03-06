from django.urls import path
from . import views


app_name = 'moodle'
urlpatterns = [
    path('', views.LessonListView.as_view(), name='index'),
    path('lesson/list/', views.LessonListView.as_view(),
         name='lesson_list'),
    path('lesson/<int:pk>/', views.LessonDetailView.as_view(),
         name='lesson_view'),
    path('lesson/add/', views.LessonAddView.as_view(), name='lesson_add'),
    path('lesson/<int:lesson_pk>/question/<int:question_pk>/answer/',
         views.QuestionAnswerFormView.as_view(),
         name='question_answer_form'),
    path('course/list/', views.CourseListView.as_view(),
         name='course_list'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(),
         name='course_view')
]
