from django.db.models import Q
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.shortcuts import redirect, render, reverse
from django.http import HttpResponse, HttpResponseForbidden

from .forms import QuestionAskForm, LessonAddForm
from .models import Course, Lesson, Question


class LessonListView(LoginRequiredMixin, generic.ListView):
    template_name = 'moodle/lesson_list.html'

    def get_queryset(self):
        return Lesson.objects.filter(
            Q(course__students__id=self.request.user.id)
            | Q(course__teachers__id=self.request.user.id)
        ).distinct()


class LessonDetailView(LoginRequiredMixin, generic.DetailView):
    model = Lesson
    template_name = 'moodle/lesson_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(
            lesson=self.get_object())
        if 'form' in self.kwargs:
            context['form'] = self.kwargs['form']
        else:
            context['form'] = QuestionAskForm()
        return context

    def post(self, request, *args, **kwargs):
        form = QuestionAskForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.lesson = self.get_object()
            question.asker = request.user
            question.save()
            return redirect('moodle:lesson_view', pk=self.get_object().pk)
        messages.error(self.request,
                       "The question has to be shorter than 500 characters.")
        return redirect('moodle:lesson_view', pk=self.get_object().pk)


class LessonAddView(LoginRequiredMixin, generic.CreateView):
    template_name = 'moodle/lesson_add_form.html'
    form_class = LessonAddForm

    def get_success_url(self):
        return reverse('moodle:lesson_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_id'] = self.request.user.id
        return kwargs


class QuestionAnswerFormView(LoginRequiredMixin, generic.UpdateView):
    fields = ('answer_text',)
    template_name = 'moodle/question_answer_form.html'

    def get_object(self):
        return Question.objects.get(pk=self.kwargs['question_pk'],
                                    lesson__pk=self.kwargs['lesson_pk'])

    def form_valid(self, form):
        self.object.answerer = self.request.user
        self.object.answer_date = timezone.now()
        form.save()
        return redirect('moodle:lesson_view', pk=self.object.lesson.id)


class CourseListView(LoginRequiredMixin, generic.ListView):
    template_name = 'moodle/course_list.html'

    def get_queryset(self):
        return Course.objects.filter(
            Q(students__id=self.request.user.id)
            | Q(teachers__id=self.request.user.id)
        ).distinct()


class CourseDetailView(LoginRequiredMixin, generic.DetailView):
    model = Course
    template_name = 'moodle/course_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = Lesson.objects.filter(
            course=self.get_object())
        return context
