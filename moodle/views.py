from django.db.models import Q
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.shortcuts import redirect, render, reverse
from django.http import HttpResponse, HttpResponseForbidden

from .forms import QuestionAskForm, LessonAddForm
from .models import Course, Lesson, Question
from .mixins import SiteTitleMixin, CourseAccessMixin, LessonAccessMixin


class LessonListView(SiteTitleMixin, LoginRequiredMixin, generic.ListView):
    """A view showing all lessons for a particular student or teacher."""
    template_name = 'moodle/lesson_list.html'
    site_title = 'Lessons'

    def get_queryset(self):
        return Lesson.objects.filter(
            Q(course__students__id=self.request.user.id)
            | Q(course__teachers__id=self.request.user.id)
        ).distinct()


class LessonDetailView(LessonAccessMixin, SiteTitleMixin,
                       LoginRequiredMixin, generic.DetailView):
    """A view showing a particular lesson in detail."""
    model = Lesson
    template_name = 'moodle/lesson_view.html'
    site_title = 'Lesson View'

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


class LessonAddView(SiteTitleMixin, LoginRequiredMixin, generic.CreateView):
    """A view that handles adding a new lesson to the database."""
    template_name = 'moodle/lesson_add_form.html'
    form_class = LessonAddForm
    site_title = 'Add Lesson'

    def get_success_url(self):
        return reverse('moodle:lesson_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_id'] = self.request.user.id
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Teachers').exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class QuestionAnswerFormView(SiteTitleMixin, LoginRequiredMixin, generic.UpdateView):
    """A view that handles a teacher answering a student's question."""
    fields = ('answer_text',)
    template_name = 'moodle/question_answer_form.html'
    site_title = 'Add Question'

    def get_object(self):
        return Question.objects.get(pk=self.kwargs['question_pk'],
                                    lesson__pk=self.kwargs['lesson_pk'])

    def form_valid(self, form):
        self.object.answerer = self.request.user
        self.object.answer_date = timezone.now()
        form.save()
        return redirect('moodle:lesson_view', pk=self.object.lesson.id)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='Teachers').exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class CourseListView(SiteTitleMixin, LoginRequiredMixin, generic.ListView):
    """A view showing all courses for a particular student or teacher."""
    template_name = 'moodle/course_list.html'
    site_title = 'Courses'

    def get_queryset(self):
        return Course.objects.filter(
            Q(students__id=self.request.user.id)
            | Q(teachers__id=self.request.user.id)
        ).distinct()


class CourseDetailView(CourseAccessMixin, SiteTitleMixin,
                       LoginRequiredMixin, generic.DetailView):
    """A view showing a particular lesson in detail."""
    model = Course
    template_name = 'moodle/course_view.html'
    site_title = 'Course View'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = Lesson.objects.filter(course=self.get_object())
        return context


def fordbidden_view(request, exception):
    return render(request, 'moodle/403.html')
