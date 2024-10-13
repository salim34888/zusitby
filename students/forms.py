from django import forms
from courses.models import Course

class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.none(),
        widget=forms.HiddenInput
    )

    def __init__(self, *args, **kwargs):
        super(CourseEnrollForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.all()


class AnswerForm(forms.Form):
    answer = forms.CharField(label='Ваш ответ', max_length=255)
    question_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)
        self.fields['answer'].label = f'Ваш ответ на вопрос: {self.question.text}' if self.question else 'Ваш ответ'
        self.fields['question_id'].initial = self.question.id
