from django import forms
from .models import Question


class QuestionAskForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('text',)
