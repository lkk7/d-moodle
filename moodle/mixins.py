from django.db.models import Q
from django.core.exceptions import PermissionDenied
from .models import Course, Lesson, Question

BASE_SITE_TITLE = 'd-moodle'


class SiteTitleMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_title'] = '{} | {}'.format(
            BASE_SITE_TITLE, self.site_title)
        return context


class CourseAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id in (
            Course.objects.get(id=self.get_object().id).students.all(
            ).values_list('id', flat=True)
            | Course.objects.get(id=self.get_object().id).teachers.all(
            ).values_list('id', flat=True)
        ):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class LessonAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id in (
            Lesson.objects.get(id=self.get_object().id).course.students.all(
            ).values_list('id', flat=True)
            | Lesson.objects.get(id=self.get_object().id).course.teachers.all(
            ).values_list('id', flat=True)
        ):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
