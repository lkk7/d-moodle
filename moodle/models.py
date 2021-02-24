from django.conf import settings
from django.db import models
from django.utils import timezone


class Course(models.Model):
    name = models.CharField(max_length=100)
    creation_date = models.DateField(default=timezone.now)
    teachers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='courses_teached')
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='courses_learned')

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(
        'moodle.Course', on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    text = models.TextField()
    publication_date = models.DateTimeField(default=timezone.now)
    modification_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Question(models.Model):
    lesson = models.ForeignKey(
        'moodle.Lesson', on_delete=models.CASCADE, related_name='questions')
    asker = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='questions_asked')
    answerer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='questions_answered', null=True, blank=True)
    text = models.TextField(max_length=1000)
    answer_text = models.TextField(blank=True)
    answered = models.BooleanField(default=False)
    ask_date = models.DateTimeField(default=timezone.now)
    answer_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '{} – {}'.format(self.lesson.title, self.id)
