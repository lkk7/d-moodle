from django.shortcuts import HttpResponse
from .models import Course, Lesson, Question
from django.views import generic
from django.db.models import Q


def index(request):
    if request.user.is_authenticated:
        return HttpResponse('index.')
    else:
        return HttpResponse('index. log in.')


class LessonListView(generic.ListView):
    template_name = 'moodle/lesson_list.html'

    def get_queryset(self):
        return Lesson.objects.filter(
            Q(course__students__id__contains=self.request.user.id)
            | Q(course__teachers__id__contains=self.request.user.id)
        ).distinct()


class LessonDetailView(generic.DetailView):
    model = Lesson
    template_name = 'moodle/lesson_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(
            lesson=self.get_object())
        return context


class CourseListView(generic.ListView):
    template_name = 'moodle/course_list.html'

    def get_queryset(self):
        return Course.objects.filter(
            Q(students__id__contains=self.request.user.id)
            | Q(teachers__id__contains=self.request.user.id)
        ).distinct()


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'moodle/course_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = Lesson.objects.filter(
            course=self.get_object())
        return context
