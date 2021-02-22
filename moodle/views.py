from django.shortcuts import HttpResponse
from .models import Course, Lesson, Question
from django.views import generic


def index(request):
    if request.user.is_authenticated:
        return HttpResponse('index.')
    else:
        return HttpResponse('index. log in.')


class LessonDetailView(generic.DetailView):
    model = Lesson
    template_name = 'moodle/lesson_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(
            lesson=self.get_object())
        return context
