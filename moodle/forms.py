from django import forms
from .models import Question, Lesson, Course


class QuestionAskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text',)


class LessonAddForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('course', 'title', 'text')

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(
            teachers__id__contains=user_id)
